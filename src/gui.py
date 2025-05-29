import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import os
import json
import logging
import time
from file_handler import FileHandler
from logger import log_message
from PIL import Image, ImageTk
from utils import hash_password, load_existing_parts, load_parts_catalogue, load_part_cost, handle_errors
from logic import calculate_and_save, generate_quote, update_rate, create_user, remove_user
from logging_config import setup_logger

logger = setup_logger('gui', 'gui.log')
TESTING_MODE = os.environ.get('TESTING_MODE', '0') == '1'
logger.debug(f"TESTING_MODE: {TESTING_MODE}")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SheetMetalClientHub:
    def __init__(self, root):
        logger.info("Initializing SheetMetalClientHub")
        if not isinstance(root, tk.Tk):
            logger.error("Invalid root: expected tk.Tk")
            raise ValueError("Root must be tk.Tk")
        self.root = root
        self.root.title("Sheet Metal Client Hub")
        self.root.geometry("1000x750")
        self.root.minsize(1050, 800)
        try:
            self.root.iconbitmap(os.path.join(BASE_DIR, 'docs/images/laser_gear.ico'))
        except tk.TclError:
            logger.warning("Could not load laser_gear.ico")
        self.file_handler = FileHandler()
        self.role = None
        self.single_selected_sub_parts = []
        self.assembly_selected_sub_parts = []
        self.added_parts = []
        self.last_part_id = None
        self.last_total_cost = None
        self.work_centre_vars = [tk.StringVar(value="") for _ in range(10)]
        self.work_centre_quantity_vars = [tk.StringVar(value="0") for _ in range(10)]
        self.work_centre_sub_option_vars = [tk.StringVar(value="None") for _ in range(10)]
        self.fastener_count_var = tk.StringVar(value="0")
        self.assembly_sub_part_quantity_var = tk.StringVar(value="1")
        self.assembly_quantity_var = tk.StringVar(value="1")
        self.single_quantity_var = tk.StringVar(value="1")
        self.assembly_sub_parts_var = tk.StringVar(value="Select Item")
        self.single_sub_parts_var = tk.StringVar(value="Select Item")
        self.single_material_var = tk.StringVar(value="Mild Steel")
        self.single_thickness_var = tk.StringVar(value="1.0")
        self.single_lay_flat_length_var = tk.StringVar(value="1000")
        self.single_lay_flat_width_var = tk.StringVar(value="500")
        self.single_weldment_var = tk.StringVar(value="No")
        self.last_clear_time = 0
        self.clear_debounce_interval = 0.5
        self.create_login_screen()

    def show_message(self, title, message, level='info'):
        logger.debug(f"Show message: {title}")
        if TESTING_MODE:
            log_message(title=title, message=message, level=level)
        else:
            messagebox.showinfo(title, message) if level == 'info' else messagebox.showerror(title, message)
        logger.log(logging.INFO if level == 'info' else logging.ERROR, f"{title}: {message}")

    def _create_header(self, parent, title):
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(side=tk.TOP, fill="x", padx=10, pady=(10, 10))
        tk.Label(frame, text=title, font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=5)
        try:
            image = Image.open(os.path.join(BASE_DIR, 'docs/images/laser_gear.png')).resize((32, 32), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=photo, bg="#f0f0f0")
            label.image = photo
            label.pack(pady=5)
            logger.debug("Loaded laser_gear.png")
        except FileNotFoundError:
            logger.warning("laser_gear.png not found")
            tk.Label(frame, text="[Logo]", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            tk.Label(frame, text="[Logo]", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)
        return frame

    def _create_panel(self, parent, place=False, **kwargs):
        frame = tk.Frame(parent, bg="#e8ecef", bd=1, relief=tk.SOLID, **kwargs)
        if place:
            frame.place(relx=0.5, rely=0.5, anchor="center")
        else:
            frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        return frame

    def _create_styled_button(self, parent, text, command, style='action', width=15):
        colors = {'action': '#28a745', 'destructive': '#dc3545', 'navigation': '#007bff', 'edit': '#ffc107'}
        bg = colors.get(style, '#28a745')
        btn = tk.Button(parent, text=text, command=command, font=("Arial", 12), bg=bg, fg="#ffffff", width=width)
        return btn

    def create_footer(self):
        logger.debug("Creating footer")
        footer = tk.Frame(self.root, bg="lightgrey")
        footer.pack(side=tk.BOTTOM, fill="x")
        tk.Label(footer, text="Version 1.0", font=("Arial", 10), bg="lightgrey").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(footer, text="Help", command=self.show_help, font=("Arial", 10), bg="lightgrey").pack(side=tk.RIGHT, padx=10, pady=5)

    def show_help(self):
        logger.info("Displaying help guide")
        guide = (
            "Sheet Metal Client Hub - User Guide\n\n"
            "1. Login: Use username/password (e.g., laurie:moffat123, admin:admin123). Check data/users.json if issues.\n"
            "2. Part Input: Enter part/assembly details, select materials, fasteners, WorkCentre operations.\n"
            "3. Quote: Generate quotes with customer name and profit margin.\n"
            "4. Admin: Manage users and rates. Rates stored in data/rates.json.\n"
            "Support: [support email]."
        )
        self.show_message("Help", guide, 'info')

    def create_widget_pair(self, parent, label_text, widget_type, row, col=0, options=None, textvariable=None, default=None, state='normal'):
        tk.Label(parent, text=label_text, font=("Arial", 12), bg="#e8ecef").grid(row=row, column=col, sticky="e", padx=(10, 2), pady=2)
        if widget_type == tk.Entry:
            widget = tk.Entry(parent, font=("Arial", 12), textvariable=textvariable, state=state)
            if default:
                widget.insert(0, default)
        elif widget_type == tk.OptionMenu:
            widget = tk.OptionMenu(parent, textvariable, *options)
        elif widget_type == tk.Listbox:
            widget = tk.Listbox(parent, font=("Arial", 12), height=options.get('height', 5), width=options.get('width', 40))
        widget.grid(row=row, column=col+1, sticky="w", padx=(2, 5), pady=2)
        return widget

    def _configure_grid(self, frame, cols=2):
        for i in range(cols):
            frame.grid_columnconfigure(i, weight=1)

    def create_login_screen(self):
        logger.info("Creating login screen")
        self.clear_screen()
        self._create_header(self.root, "Login")
        main_frame = self._create_panel(self.root, place=True)
        self.username_entry = self.create_widget_pair(main_frame, "Username:", tk.Entry, row=0)
        self.username_entry.focus_set()
        self.password_entry = self.create_widget_pair(main_frame, "Password:", tk.Entry, row=1)
        self.password_entry.config(show="*")
        self._create_styled_button(main_frame, "Login", self.login).grid(row=2, column=0, padx=5, pady=10)
        self._create_styled_button(main_frame, "Clear", lambda: self.clear_fields([(self.username_entry, ""), (self.password_entry, "")], "Clearing login fields", "FR1"), style='navigation').grid(row=2, column=1, padx=5, pady=10)
        self.root.bind('<Return>', lambda event: self.login())
        self._configure_grid(main_frame)
        self.create_footer()

    def clear_fields(self, field_pairs, log_msg, test_case):
        logger.info(log_msg)
        for field, default in field_pairs:
            try:
                if isinstance(field, tk.Entry) and field.winfo_exists():
                    field.delete(0, tk.END)
                    if default:
                        field.insert(0, default)
                elif isinstance(field, tk.StringVar):
                    field.set(default)
                elif isinstance(field, tk.Listbox) and field.winfo_exists():
                    field.delete(0, tk.END)
            except tk.TclError as e:
                logger.warning(f"Error clearing field: {e}")

    @handle_errors("FR1: Login", lambda self: f"Username: {getattr(self, 'username_entry', {'get': lambda: ''}).get().strip()}")
    def login(self):
        logger.info("Attempting login")
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            logger.error("Empty credentials")
            raise ValueError("Username and password cannot be empty")
        
        hashed_password = hash_password(password)
        if not hashed_password:
            logger.error(f"Hash failed for {username}")
            raise ValueError("Error processing password")
        
        try:
            users_file = os.path.join(BASE_DIR, 'data', 'users.json')
            if not os.path.exists(users_file):
                logger.error(f"Users file missing: {users_file}")
                raise FileNotFoundError("Users file not found")
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            if self.file_handler.validate_credentials(username, hashed_password):
                self.role = self.file_handler.get_user_role(username)
                if not self.role:
                    logger.error(f"No role for {username}")
                    raise ValueError("User role not found")
                logger.info(f"Login successful as {self.role}")
                if self.role == "User":
                    self.create_part_input_screen()
                else:
                    self.create_admin_screen()
                return f"Login successful as {self.role}"
            else:
                logger.error(f"Invalid credentials for {username}")
                raise ValueError("Invalid username or password")
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise ValueError(f"Authentication error: {str(e)}")

    def prompt_admin_create(self):
        logger.info("Prompting admin credentials")
        if TESTING_MODE:
            log_message(title='Admin', message='Bypassing admin prompt', level='info')
            return True

        dialog = tk.Toplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        self._create_header(dialog, "Admin Login")
        main_frame = self._create_panel(dialog)
        username_entry = self.create_widget_pair(main_frame, "Admin Username:", tk.Entry, row=0)
        username_entry.focus_set()
        password_entry = self.create_widget_pair(main_frame, "Admin Password:", tk.Entry, row=1)
        password_entry.config(show="*")

        result = {"valid": False}

        def validate():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                self.show_message("Error", "Credentials cannot be empty", 'error')
                return
            hashed_password = hash_password(password)
            if not hashed_password:
                logger.error(f"Hash failed for {username}")
                self.show_message("Error", "Error processing credentials", 'error')
                return
            try:
                if self.file_handler.validate_credentials(username, hashed_password) and self.file_handler.get_user_role(username) == "Admin":
                    logger.info(f"Admin validated: {username}")
                    result["valid"] = True
                    dialog.destroy()
                else:
                    logger.error(f"Invalid admin credentials: {username}")
                    self.show_message("Error", "Invalid admin credentials", 'error')
            except Exception as e:
                logger.error(f"Validation error: {e}")
                self.show_message("Error", f"Authentication error: {str(e)}", 'error')

        self._create_styled_button(main_frame, "Submit", validate).grid(row=2, column=0, padx=5, pady=10)
        self._create_styled_button(main_frame, "Cancel", dialog.destroy, style='navigation').grid(row=2, column=1, padx=5, pady=10)
        dialog.bind('<Return>', lambda event: validate())
        self._configure_grid(main_frame)
        self.root.wait_window(dialog)
        return result["valid"]

    def update_quantity_entry_state(self):
        logger.debug("Updating quantity entry state")
        for var, entry in [(self.assembly_quantity_var, self.assembly_custom_quantity_entry), 
                          (self.single_quantity_var, self.single_custom_quantity_entry)]:
            entry.config(state='normal' if var.get() == "Other" else 'disabled')

    def update_sub_parts_dropdown(self, tab_index):
        logger.debug(f"Updating sub-parts dropdown: tab {tab_index}")
        var, option = (self.single_sub_parts_var, self.single_sub_parts_option) if tab_index == 1 else (self.assembly_sub_parts_var, self.assembly_sub_parts_option)
        var.set("Select Item")
        menu = option['menu']
        menu.delete(0, tk.END)
        menu.add_command(label="Select Item", command=lambda: var.set("Select Item"))
        items = load_parts_catalogue() if tab_index == 1 else load_existing_parts()
        if tab_index == 1:
            for item_id, desc, price in items or []:
                label = f"{item_id}: {desc}"
                menu.add_command(label=label, command=lambda x=label: var.set(x))
        else:
            for item in items or []:
                menu.add_command(label=item, command=lambda x=item: var.set(x))
        if not items:
            menu.add_command(label="No items available", command=lambda: var.set("No items available"))

    def update_selected_items(self, tab_index):
        logger.debug(f"Updating selected items: tab {tab_index}")
        listbox = self.single_selected_sub_parts_listbox if tab_index == 1 else self.assembly_selected_sub_parts_listbox
        listbox.delete(0, tk.END)
        if tab_index == 1:
            listbox.insert(tk.END, self.single_material_var.get())
            for item_id, desc, count in self.single_selected_sub_parts:
                listbox.insert(tk.END, f"{item_id}: {desc} ({count})" if count > 1 else f"{item_id}: {desc}")
        else:
            for part_id, qty in self.assembly_selected_sub_parts:
                listbox.insert(tk.END, f"{part_id} ({qty})" if qty > 1 else part_id)

    def add_sub_part(self, tab_index):
        logger.debug(f"Adding sub-part: tab {tab_index}")
        if tab_index == 1:
            selected_item = self.single_sub_parts_var.get()
            selected_list = self.single_selected_sub_parts
            if selected_item and selected_item not in ["Select Item", "No catalogue items available"]:
                try:
                    item_id, desc = selected_item.split(": ", 1)
                except ValueError:
                    item_id = selected_item
                    desc = item_id
                count = int(self.fastener_count_var.get() or 0)
                if count > 0:
                    for i, (eid, edesc, ec) in enumerate(selected_list):
                        if eid == item_id:
                            selected_list[i] = (item_id, desc, ec + count)
                            break
                    else:
                        selected_list.append((item_id, desc, count))
                self.single_sub_parts_var.set("Select Item")
        else:
            selected_item = self.assembly_sub_parts_var.get()
            selected_list = self.assembly_selected_sub_parts
            qty = int(self.assembly_sub_part_quantity_var.get() or 1)
            if selected_item and selected_item not in ["Select Item", "No parts available"]:
                for i, (pid, pq) in enumerate(selected_list):
                    if pid == selected_item:
                        selected_list[i] = (selected_item, pq + qty)
                        break
                else:
                    selected_list.append((selected_item, qty))
                self.assembly_sub_parts_var.set("Select Item")
                self.assembly_sub_part_quantity_var.set("1")
        self.update_selected_items(tab_index)

    def clear_sub_parts(self, tab_index):
        logger.debug(f"Clearing sub-parts: tab {tab_index}")
        fields = [(self.single_selected_sub_parts_listbox, None), (self.fastener_count_var, "0")] if tab_index == 1 else [(self.assembly_selected_sub_parts_listbox, None)]
        self.clear_fields(fields, f"Clearing sub-parts: tab {tab_index}", f"Clear Sub-Parts Tab {tab_index}")
        if tab_index == 1:
            self.single_selected_sub_parts = []
        else:
            self.assembly_selected_sub_parts = []

    def update_quantity_dropdown(self, index, work_centre):
        logger.debug(f"Updating quantity dropdown: index {index}, work_centre {work_centre}")
        qty_dropdown = self.quantity_dropdowns[index]
        qty_var = self.work_centre_quantity_vars[index]
        sub_option_var = self.work_centre_sub_option_vars[index]
        qty_var.set("0")
        sub_option_var.set("None")

        for i, var in enumerate(self.work_centre_vars):
            if i != index and var.get() == work_centre and work_centre:
                current_qty = float(self.work_centre_quantity_vars[i].get() or 0)
                self.work_centre_quantity_vars[i].set(str(current_qty + 100))
                self.work_centre_vars[index].set("")
                qty_dropdown.grid_remove()
                self.update_selected_items(self.notebook.index(self.notebook.select()))
                return

        qty_menu = qty_dropdown['menu']
        qty_menu.delete(0, tk.END)
        if hasattr(self, f'sub_option_dropdown_{index}'):
            getattr(self, f'sub_option_dropdown_{index}').grid_remove()

        if not work_centre:
            qty_dropdown.grid_remove()
            return

        qty_dropdown.grid(row=index+1, column=2, sticky="w", padx=(2, 5), pady=2)
        quantities, label = self.get_quantity_options(work_centre)
        qty_menu.add_command(label=f"{label}: 0", command=lambda: qty_var.set("0"))
        for qty in quantities:
            qty_menu.add_command(label=f"{label}: {qty}", command=lambda x=qty: qty_var.set(str(x)))

        if work_centre in ["Welding", "Coating"]:
            sub_options = ["None", "MIG", "TIG"] if work_centre == "Welding" else ["None", "Painting", "Coating"]
            sub_option_dropdown = tk.OptionMenu(self.operations_frame, sub_option_var, *sub_options)
            sub_option_dropdown.grid(row=index+1, column=3, sticky="w", padx=(2, 5), pady=2)
            setattr(self, f'sub_option_dropdown_{index}', sub_option_dropdown)

        self.update_selected_items(self.notebook.index(self.notebook.select()))

    def get_quantity_options(self, work_centre):
        options = {
            "Cutting": ([100, 500, 1000, 2000, 3000], "Cutting Length (mm)"),
            "Bending": ([1, 2, 5, 10, 20], "Number of Bends"),
            "Welding": ([100, 500, 1000, 2000], "Weld Length (mm)"),
            "Assembly": ([1, 2, 5, 10], "Number of Components"),
            "Finishing": ([1000, 5000, 10000, 20000], "Surface Area (mm²)"),
            "Drilling": ([1, 5, 10, 20], "Number of Holes"),
            "Punching": ([1, 5, 10, 20], "Number of Punches"),
            "Grinding": ([1000, 5000, 10000, 20000], "Surface Area (mm²)"),
            "Coating": ([1000, 5000, 10000, 20000], "Surface Area to be Painted (mm²)"),
            "Inspection": ([1, 2, 5], "Number of Inspections")
        }
        return options.get(work_centre, ([0], "Quantity"))

    def go_to_settings(self):
        logger.info("Navigating to settings")
        if self.role == "Admin" or self.prompt_admin_create():
            self.role = "Admin"
            self.create_admin_screen()
        else:
            self.show_message("Error", "Admin access denied", 'error')

    def go_back_to_login(self):
        logger.info("Returning to login")
        self.role = None
        self.create_login_screen()

    def clear_input_parameters(self):
        logger.info("Clearing input parameters")
        fields = [
            (self.part_id_entry, "ASSY-"), (self.revision_entry, ""),
            (self.single_material_var, "Mild Steel"), (self.single_thickness_var, "1.0"),
            (self.single_lay_flat_length_var, "1000"), (self.single_lay_flat_width_var, "500"),
            (self.single_weldment_var, "No"), (self.single_quantity_var, "1"),
            (self.single_custom_quantity_entry, ""), (self.single_selected_sub_parts_listbox, None),
            (self.fastener_count_var, "0"),
            (self.single_sub_parts_var, "Select Item"), (self.assembly_quantity_var, "1"),
            (self.assembly_custom_quantity_entry, ""), (self.assembly_selected_sub_parts_listbox, None),
            (self.assembly_sub_parts_var, "Select Item"), (self.assembly_sub_part_quantity_var, "1"),
        ] + [(v, "") for v in self.work_centre_vars] + [(v, "0") for v in self.work_centre_quantity_vars] + [(v, "None") for v in self.work_centre_sub_option_vars]
        self.clear_fields(fields, "Clearing input parameters", "Clear Input Parameters")
        self.notebook.select(0)
        for dropdown in self.quantity_dropdowns:
            dropdown.grid_remove()
        for i in range(10):
            if hasattr(self, f'sub_option_dropdown_{i}'):
                getattr(self, f'sub_option_dropdown_{i}').grid_remove()
        for btn in [self.submit_button, self.add_another_part_button, self.add_to_parts_list_button]:
            btn.config(state='disabled')

    def add_part_to_list(self, part_id, quantity):
        logger.info(f"Adding part {part_id} (qty: {quantity})")
        self.added_parts.append({'part_id': part_id, 'quantity': quantity})
        if hasattr(self, 'parts_list_listbox') and self.parts_list_listbox.winfo_exists():
            self.parts_list_listbox.insert(tk.END, f"{part_id} ({quantity})" if quantity > 1 else part_id)
        if len(self.added_parts) > 0 and hasattr(self, 'submit_button'):
            self.submit_button.config(state='normal')

    def open_part_search_popup(self):
        logger.info("Opening part search pop-up")
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Part from Database")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        self._create_header(dialog, "Add Part from Database")
        main_frame = self._create_panel(dialog)
        search_var = tk.StringVar()
        search_entry = self.create_widget_pair(main_frame, "Search Parts:", tk.Entry, row=0, textvariable=search_var)
        search_entry.focus_set()

        parts_listbox = self.create_widget_pair(main_frame, "", tk.Listbox, row=1, options={'height': 10, 'width': 30})
        parts_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
        parts_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=parts_listbox.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")

        quantity_var = tk.StringVar(value="1")
        self.create_widget_pair(main_frame, "Quantity:", tk.OptionMenu, row=2, options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], textvariable=quantity_var)

        def update_parts_list(event=None):
            search_term = search_var.get().lower()
            parts_listbox.delete(0, tk.END)
            for part in load_existing_parts():
                if search_term in part.lower():
                    parts_listbox.insert(tk.END, part)

        def add_selected_part():
            selection = parts_listbox.curselection()
            if not selection:
                self.show_message("Error", "Select a part", 'error')
                return
            part_id = parts_listbox.get(selection[0])
            quantity = int(quantity_var.get())
            self.add_part_to_list(part_id, quantity)
            self.show_message("Success", f"Added {part_id} (Qty: {quantity})", 'info')
            dialog.destroy()

        self._create_styled_button(main_frame, "Add Part", add_selected_part).grid(row=3, column=0, padx=5, pady=10)
        self._create_styled_button(main_frame, "Cancel", dialog.destroy, style='navigation').grid(row=3, column=1, padx=5, pady=10)
        update_parts_list()
        search_entry.bind('<KeyRelease>', update_parts_list)
        dialog.bind('<Return>', lambda event: add_selected_part())
        self._configure_grid(main_frame)

    def clear_parts_list(self):
        current_time = time.time()
        if current_time - self.last_clear_time < self.clear_debounce_interval:
            logger.debug("Debouncing clear_parts_list")
            return
        self.last_clear_time = current_time
        logger.info("Clearing parts list")
        if hasattr(self, 'parts_list_listbox') and self.parts_list_listbox.winfo_exists():
            self.clear_fields([(self.parts_list_listbox, None)], "Clearing parts list", "Clear Parts List")
        self.added_parts = []
        if hasattr(self, 'submit_button'):
            self.submit_button.config(state='disabled')

    def update_parts_list_display(self):
        if hasattr(self, 'parts_list_listbox') and self.parts_list_listbox.winfo_exists():
            self.parts_list_listbox.delete(0, tk.END)
            for part in self.added_parts:
                qty = part.get('quantity', 1)
                self.parts_list_listbox.insert(tk.END, f"{part['part_id']} ({qty})" if qty > 1 else part['part_id'])
            logger.debug("Updated parts list display")

    def create_part_input_screen(self):
        logger.info("Creating part input screen")
        self.clear_screen()
        self._create_header(self.root, "Manufacturing Input Screen")
        main_frame = self._create_panel(self.root)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)

        # Left panel
        left_frame = tk.Frame(main_frame, bg="#e8ecef")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        input_frame = tk.Frame(left_frame, bg="#e8ecef")
        input_frame.pack(side=tk.RIGHT, padx=10, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(input_frame, text="Planned Materials", font=("Arial", 14, "bold"), bg="#e8ecef").grid(row=0, column=0, columnspan=2, pady=5)

        self.part_id_entry = self.create_widget_pair(input_frame, "Part ID:", tk.Entry, row=1, default="ASSY-")
        self.revision_entry = self.create_widget_pair(input_frame, "Revision:", tk.Entry, row=2)

        self.notebook = ttk.Notebook(input_frame)
        self.notebook.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        # Assembly tab
        self.assembly_part_frame = tk.Frame(self.notebook, bg="#e8ecef")
        self.notebook.add(self.assembly_part_frame, text="Assembly")
        self.assembly_quantity_option = self.create_widget_pair(self.assembly_part_frame, "Quantity:", tk.OptionMenu, row=0, textvariable=self.assembly_quantity_var, options=["1", "5", "10", "20", "50", "100", "Other"])
        self.assembly_custom_quantity_entry = self.create_widget_pair(self.assembly_part_frame, "", tk.Entry, row=1, state='disabled')
        self.assembly_sub_parts_option = self.create_widget_pair(self.assembly_part_frame, "Sub-Parts:", tk.OptionMenu, row=2, textvariable=self.assembly_sub_parts_var, options=["Select Item"])
        self.assembly_sub_part_quantity_option = self.create_widget_pair(self.assembly_part_frame, "Sub-Part Qty:", tk.OptionMenu, row=3, textvariable=self.assembly_sub_part_quantity_var, options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self._create_styled_button(self.assembly_part_frame, "Add Sub-Part", lambda: self.add_sub_part(0)).grid(row=4, column=1, sticky="w", padx=(2, 5), pady=2)
        self._create_styled_button(self.assembly_part_frame, "Clear Selected", lambda: self.clear_sub_parts(0), style='navigation').grid(row=5, column=1, sticky="w", padx=(2, 5), pady=2)
        listbox_frame = tk.Frame(self.assembly_part_frame, bg="#e8ecef")
        self.assembly_selected_sub_parts_listbox = tk.Listbox(listbox_frame, font=("Arial", 12), height=5, width=40)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.assembly_selected_sub_parts_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.assembly_selected_sub_parts_listbox.yview)
        self.assembly_selected_sub_parts_listbox.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox_frame.grid(row=6, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=2)

        self.assembly_quantity_var.trace("w", lambda *args: self.update_quantity_entry_state())

        # Single Part tab
        self.single_part_frame = tk.Frame(self.notebook, bg="#e8ecef")
        self.notebook.add(self.single_part_frame, text="Single Part")
        self.single_material_option = self.create_widget_pair(self.single_part_frame, "Material:", tk.OptionMenu, row=0, textvariable=self.single_material_var, options=["Mild Steel", "Aluminium", "Stainless Steel"])
        self.single_thickness_option = self.create_widget_pair(self.single_part_frame, "Thickness (mm):", tk.OptionMenu, row=1, textvariable=self.single_thickness_var, options=["1.0", "1.2", "1.5", "2.0", "2.5", "3.0"])
        self.single_lay_flat_length_option = self.create_widget_pair(self.single_part_frame, "Lay-Flat Length (mm):", tk.OptionMenu, row=2, textvariable=self.single_lay_flat_length_var, options=["50", "100", "500", "1000", "1500", "2000", "3000"])
        self.single_lay_flat_width_option = self.create_widget_pair(self.single_part_frame, "Lay-Flat Width (mm):", tk.OptionMenu, row=3, textvariable=self.single_lay_flat_width_var, options=["50", "100", "500", "1000", "1500"])
        self.single_quantity_option = self.create_widget_pair(self.single_part_frame, "Quantity:", tk.OptionMenu, row=4, textvariable=self.single_quantity_var, options=["1", "5", "10", "20", "50", "100", "Other"])
        self.single_custom_quantity_entry = self.create_widget_pair(self.single_part_frame, "", tk.Entry, row=5, state='disabled')
        self.single_weldment_option = self.create_widget_pair(self.single_part_frame, "Weldment Indicator:", tk.OptionMenu, row=6, textvariable=self.single_weldment_var, options=["Yes", "No"])
        self.single_sub_parts_option = self.create_widget_pair(self.single_part_frame, "Fasteners/Inserts:", tk.OptionMenu, row=7, textvariable=self.single_sub_parts_var, options=["Select Item"])
        self.fastener_count_entry = self.create_widget_pair(self.single_part_frame, "Fastener Count:", tk.Entry, row=8, textvariable=self.fastener_count_var)
        self._create_styled_button(self.single_part_frame, "Add Fastener/Insert", lambda: self.add_sub_part(1)).grid(row=9, column=1, sticky="w", padx=(2, 5), pady=2)
        self._create_styled_button(self.single_part_frame, "Clear Selected", lambda: self.clear_sub_parts(1), style='navigation').grid(row=10, column=1, sticky="w", padx=(2, 5), pady=2)
        listbox_frame = tk.Frame(self.single_part_frame, bg="#e8ecef")
        self.single_selected_sub_parts_listbox = tk.Listbox(listbox_frame, font=("Arial", 12), height=5, width=40)
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.single_selected_sub_parts_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.single_selected_sub_parts_listbox.yview)
        self.single_selected_sub_parts_listbox.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox_frame.grid(row=11, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=2)

        self.single_material_var.trace("w", lambda *args: self.update_selected_items(1))
        self.single_quantity_var.trace("w", lambda *args: self.update_quantity_entry_state())
        self.fastener_count_var.trace("w", lambda *args: self.update_selected_items(1))

        # Separator
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.grid(row=0, column=1, sticky="ns", padx=5)

        # Right panel
        right_frame = tk.Frame(main_frame, bg="#e8ecef")
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        self.operations_frame = tk.Frame(right_frame, bg="#e8ecef")
        self.operations_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)
        tk.Label(self.operations_frame, text="Planned Operations", font=("Arial", 14, "bold"), bg="#e8ecef").grid(row=0, column=0, columnspan=4, pady=5)

        work_centres = ["", "Cutting", "Bending", "Welding", "Assembly", "Finishing", "Drilling", "Punching", "Grinding", "Coating", "Inspection"]
        self.quantity_dropdowns = []
        for i in range(10):
            tk.Label(self.operations_frame, text=f"Operation {(i+1)*10}:", font=("Arial", 10), bg="#e8ecef").grid(row=i+1, column=0, sticky="w", padx=(5, 2), pady=2)
            dropdown = tk.OptionMenu(self.operations_frame, self.work_centre_vars[i], *work_centres, command=lambda wc, idx=i: self.update_quantity_dropdown(idx, wc))
            dropdown.grid(row=i+1, column=1, sticky="w", padx=(2, 5), pady=2)
            qty_dropdown = tk.OptionMenu(self.operations_frame, self.work_centre_quantity_vars[i], "0")
            qty_dropdown.grid_remove()
            self.quantity_dropdowns.append(qty_dropdown)

        self.calculate_cost_button = self._create_styled_button(self.operations_frame, "Calculate Cost & Add Part", self.calculate_and_save, width=20)
        self.calculate_cost_button.grid(row=11, column=0, columnspan=4, pady=5)

        buttons_subframe = tk.Frame(self.operations_frame, bg="#e8ecef")
        buttons_subframe.grid(row=12, column=0, columnspan=4, pady=5)
        self.add_another_part_button = self._create_styled_button(buttons_subframe, "Screen Reset", self.clear_input_parameters, style='action', width=12)
        self.add_another_part_button.pack(side=tk.LEFT, padx=5)
        self.add_another_part_button.config(state='disabled')
        self.add_to_parts_list_button = self._create_styled_button(buttons_subframe, "Add Part to List", self.open_part_search_popup, style='action', width=12)
        self.add_to_parts_list_button.pack(side=tk.LEFT, padx=5)
        self.clear_parts_list_button = self._create_styled_button(buttons_subframe, "Clear Parts List", self.clear_parts_list, style='navigation', width=12)
        self.clear_parts_list_button.pack(side=tk.LEFT, padx=5)
        self.submit_button = self._create_styled_button(buttons_subframe, "Quote", self.create_quote_screen, style='action', width=12)
        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.submit_button.config(state='disabled')

        parts_list_frame = tk.Frame(self.operations_frame, bg="#e8ecef")
        self.parts_list_listbox = tk.Listbox(parts_list_frame, font=("Arial", 10), height=5, width=40)
        scrollbar = tk.Scrollbar(parts_list_frame, orient=tk.VERTICAL)
        self.parts_list_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.parts_list_listbox.yview)
        self.parts_list_listbox.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        parts_list_frame.grid(row=13, column=0, columnspan=4, pady=5)

        bottom_frame = tk.Frame(main_frame, bg="#e8ecef")
        bottom_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        self.settings_button = self._create_styled_button(bottom_frame, "Settings", self.go_to_settings, style='navigation')
        self.back_button = self._create_styled_button(bottom_frame, "Back to Login", self.go_back_to_login, style='navigation')
        self.settings_button.pack(side=tk.LEFT, padx=10)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.create_footer()
        self.update_sub_parts_dropdown(0)
        self.update_sub_parts_dropdown(1)
        self.update_parts_list_display()

    def on_tab_changed(self, event):
        logger.debug("Tab changed")
        selected_tab = self.notebook.index(self.notebook.select())
        self.update_sub_parts_dropdown(selected_tab)
        self.part_id_entry.delete(0, tk.END)
        self.part_id_entry.insert(0, "ASSY-" if selected_tab == 0 else "PART-")
        self.update_selected_items(selected_tab)

    @handle_errors("FR3-FR4-FR5: Cost calculation", lambda self: f"Part Type: {'Single Part' if self.notebook.index(self.notebook.select()) == 1 else 'Assembly'}, Part ID: {self.part_id_entry.get().strip()}")
    def calculate_and_save(self):
        logger.info("Calculating part specs")
        selected_tab = self.notebook.index(self.notebook.select())
        part_type = "Single Part" if selected_tab == 1 else "Assembly"
        part_id = self.part_id_entry.get().strip()
        revision = self.revision_entry.get().strip()

        specs = {
            'material': self.single_material_var.get() if selected_tab == 1 else "N/A",
            'thickness': float(self.single_thickness_var.get()) if selected_tab == 1 else 0.0,
            'length': int(self.single_lay_flat_length_var.get()) if selected_tab == 1 else 0,
            'width': int(self.single_lay_flat_width_var.get()) if selected_tab == 1 else 0,
            'quantity': int(self.single_custom_quantity_entry.get().strip() if self.single_quantity_var.get() == "Other" else self.single_quantity_var.get()) if selected_tab == 1 else int(self.assembly_custom_quantity_entry.get().strip() if self.assembly_quantity_var.get() == "Other" else self.assembly_quantity_var.get()),
            'weldment_indicator': self.single_weldment_var.get() if selected_tab == 1 else "No",
            'sub_parts': self.single_selected_sub_parts if selected_tab == 1 else self.assembly_selected_sub_parts,
            'fastener_types_and_counts': [],
            'top_level_assembly': "N/A" if selected_tab == 1 else part_id
        }

        work_centres = []
        for i, (wc, qty, sub) in enumerate(zip(self.work_centre_vars, self.work_centre_quantity_vars, self.work_centre_sub_option_vars)):
            if wc.get():
                if qty.get() == "0":
                    raise ValueError(f"Quantity for {wc.get()} in Operation {(i+1)*10} required")
                if wc.get() in ["Welding", "Coating"] and sub.get() == "None":
                    raise ValueError(f"{'Weld type' if wc.get() == 'Welding' else 'Surface treatment type'} required for {wc.get()}")
                work_centres.append((wc.get(), float(qty.get()), sub.get()))

        part_specs = {'part_type': part_type, 'part_id': part_id, 'revision': revision, 'specs': specs, 'work_centres': work_centres}
        rates = self.file_handler.load_rates()
        total_cost = calculate_and_save(part_specs, self.file_handler, rates, self.added_parts, self.show_message)
        self.submit_button.config(state='normal')
        self.add_another_part_button.config(state='normal')
        self.add_to_parts_list_button.config(state='normal')
        self.last_part_id = part_id
        self.last_total_cost = total_cost
        self.add_part_to_list(part_id, specs['quantity'])

    def create_quote_screen(self):
        logger.info("Creating quote screen")
        self.clear_screen()
        self._create_header(self.root, "Generate Quote")
        main_frame = self._create_panel(self.root)
        self.customer_entry = self.create_widget_pair(main_frame, "Customer Name:", tk.Entry, row=0)
        self.margin_entry = self.create_widget_pair(main_frame, "Profit Margin (%):", tk.Entry, row=1)
        self._create_styled_button(main_frame, "Generate Quote", self.generate_quote).grid(row=2, column=0, columnspan=2, pady=10)

        table_frame = tk.Frame(main_frame, bg="#e8ecef")
        table_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="ew")
        tk.Label(table_frame, text="Parts Summary", font=("Arial", 12, "bold"), bg="#e8ecef").pack(pady=(0, 5))

        style = ttk.Style()
        style.configure("Quote.Treeview", font=("Arial", 12), rowheight=25)
        style.configure("Quote.Treeview.Heading", font=("Arial", 12, "bold"))

        columns = ("Part ID", "Quantity", "Unit Cost", "Total Cost")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Quote.Treeview", height=10)
        for col in columns:
            tree.heading(col, text=col)
        tree.column("Part ID", width=200, anchor="w")
        tree.column("Quantity", width=100, anchor="center")
        tree.column("Unit Cost", width=150, anchor="e")
        tree.column("Total Cost", width=150, anchor="e")
        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        total_sum = 0.0
        for part in self.added_parts:
            part_id = part['part_id']
            quantity = part['quantity']
            unit_cost = load_part_cost(part_id)
            if unit_cost is None:
                raise ValueError(f"Cost not found for part {part_id}")
            total_cost = unit_cost * quantity
            total_sum += total_cost
            tree.insert("", tk.END, values=(part_id, quantity, f"{unit_cost:.2f}", f"{total_cost:.2f}"))

        tk.Label(table_frame, text=f"Total: £{total_sum:.2f}", font=("Arial", 12, "bold"), bg="#e8ecef").pack(pady=(5, 0))
        self.create_footer()

    @handle_errors("FR7: Generate quote", lambda self: f"Customer: {getattr(self, 'customer_entry', {'get': lambda: ''}).get().strip()}")
    def generate_quote(self):
        logger.info("Generating quote")
        customer_name = self.customer_entry.get().strip()
        profit_margin = self.margin_entry.get().strip()
        generate_quote(customer_name, profit_margin, self.added_parts, self.file_handler, self.show_message)
        self.root.update()
        self.create_part_input_screen()
        self.clear_parts_list()

    def create_admin_screen(self):
        logger.info("Creating admin screen")
        self.clear_screen()
        self._create_header(self.root, "Admin Settings")
        main_frame = self._create_panel(self.root)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Rate Management
        rate_frame = tk.Frame(main_frame, bg="#e8ecef", bd=1, relief=tk.SOLID)
        rate_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=10)
        tk.Label(rate_frame, text="Rate Management", font=("Arial", 14, "bold"), bg="#e8ecef").grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))

        self.rate_key_var = tk.StringVar(value="Select Rate Key")
        try:
            rates = self.file_handler.load_rates()
            rate_keys = list(rates.keys())
        except ValueError as e:
            self.show_message("Error", f"Failed to load rates: {str(e)}", 'error')
            rate_keys = []
            logger.error(f"Rate load error: {e}")
        rate_key_dropdown = self.create_widget_pair(rate_frame, "Rate Key:", tk.OptionMenu, row=1, col=0, options=["Select Rate Key"] + rate_keys, textvariable=self.rate_key_var)
        self._create_styled_button(rate_frame, "Update Rate", self.update_rate).grid(row=1, column=2, padx=5, pady=5)

        self.rate_value_var = tk.StringVar()
        self.rate_sub_value_var = tk.StringVar()
        self.rate_value_frame = tk.Frame(rate_frame, bg="#e8ecef")
        self.rate_value_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        def update_rate_fields(*args):
            logger.debug("Updating rate fields")
            for widget in self.rate_value_frame.winfo_children():
                widget.destroy()
            rate_key = self.rate_key_var.get()
            if rate_key not in rates:
                return
            config = rates[rate_key]
            rate_type = config.get('type', 'simple')
            unit = config.get('unit', '£/unit')
            self.create_widget_pair(self.rate_value_frame, f"Rate Value ({unit}):", tk.Entry, row=0, col=0, textvariable=self.rate_value_var)
            if rate_type == 'hourly' and 'sub_field' in config:
                self.create_widget_pair(self.rate_value_frame, f"{config['sub_field']}:", tk.Entry, row=1, col=0, textvariable=self.rate_sub_value_var)

        self.rate_key_var.trace("w", update_rate_fields)
        update_rate_fields()

        # User Management
        user_frame = tk.Frame(main_frame, bg="#e8ecef", bd=1, relief=tk.SOLID)
        user_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        tk.Label(user_frame, text="User Management", font=("Arial", 14, "bold"), bg="#e8ecef").grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))

        self.new_username_var = tk.StringVar()
        self.new_password_var = tk.StringVar()
        self.new_role_var = tk.StringVar(value="User")
        self.create_widget_pair(user_frame, "Role:", tk.OptionMenu, row=1, col=0, options=["User", "Admin"], textvariable=self.new_role_var)
        self.create_widget_pair(user_frame, "New Username:", tk.Entry, row=2, col=0, textvariable=self.new_username_var)
        self.create_widget_pair(user_frame, "New Password:", tk.Entry, row=3, col=0, textvariable=self.new_password_var).config(show="*")
        self._create_styled_button(user_frame, "Create User", self.create_user).grid(row=1, column=2, padx=5, pady=5)

        self.edit_username_var = tk.StringVar(value="Select User")
        users = self.file_handler.get_all_usernames()
        self.edit_user_dropdown = self.create_widget_pair(user_frame, "Edit User:", tk.OptionMenu, row=4, col=0, options=["Select User"] + users, textvariable=self.edit_username_var)
        self._create_styled_button(user_frame, "Edit User", self.edit_user, style='edit').grid(row=4, column=2, padx=5, pady=5)

        self.remove_username_var = tk.StringVar(value="Select User")
        self.remove_user_dropdown = self.create_widget_pair(user_frame, "Remove User:", tk.OptionMenu, row=5, col=0, options=["Select User"] + users, textvariable=self.remove_username_var)
        self._create_styled_button(user_frame, "Remove User", self.remove_user, style='destructive').grid(row=5, column=2, padx=5, pady=5)

        def update_user_dropdowns(*args):
            logger.debug("Updating user dropdowns")
            users = self.file_handler.get_all_usernames()
            for var, dropdown in [(self.edit_username_var, self.edit_user_dropdown), (self.remove_username_var, self.remove_user_dropdown)]:
                var.set("Select User")
                menu = dropdown['menu']
                menu.delete(0, tk.END)
                menu.add_command(label="Select User", command=lambda v=var: v.set("Select User"))
                for user in users:
                    menu.add_command(label=user, command=lambda u=user, v=var: v.set(u))

        self.new_username_var.trace("w", update_user_dropdowns)
        nav_frame = tk.Frame(self.root, bg="#e8ecef")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        self._create_styled_button(nav_frame, "User Features", self.create_part_input_screen, style='navigation').pack(side=tk.LEFT, padx=10)
        self._create_styled_button(nav_frame, "Back to Login", self.go_back_to_login, style='navigation').pack(side=tk.LEFT, padx=10)
        self.create_footer()

    @handle_errors("Create User", lambda self: f"Username: {self.new_username_var.get().strip()}")
    def create_user(self):
        logger.info("Creating user")
        username = self.new_username_var.get().strip()
        password = self.new_password_var.get().strip()
        role = self.new_role_var.get()
        create_user(username, password, role, self.file_handler, self.show_message)
        self.new_username_var.set("")
        self.new_password_var.set("")
        self.new_role_var.set("User")

    @handle_errors("Remove User", lambda self: f"Username: {self.remove_username_var.get().strip()}")
    def remove_user(self):
        logger.info("Removing user")
        username = self.remove_username_var.get().strip()
        remove_user(username, self.file_handler, self.show_message)
        self.remove_username_var.set("Select User")

    @handle_errors("FR6: Update rate", lambda self: f"Rate Key: {self.rate_key_var.get()}")
    def update_rate(self):
        logger.info("Updating rate")
        rate_key = self.rate_key_var.get()
        rate_value = self.rate_value_var.get().strip()
        sub_value = self.rate_sub_value_var.get().strip()
        update_rate(rate_key, rate_value, sub_value, self.file_handler, self.show_message)
        self.rate_value_var.set("")
        self.rate_sub_value_var.set("")

    @handle_errors("Edit User", lambda self: f"Username: {self.edit_username_var.get().strip()}")
    def edit_user(self):
        logger.info("Attempting to edit user")
        username = self.edit_username_var.get().strip()
        if username == "Select User":
            self.show_message("Error", "Select a user to edit", 'error')
            logger.error("No user selected")
            return
        self.show_message("Info", f"Edit user for {username} not implemented", 'info')
        self.edit_username_var.set("Select User")

    def clear_screen(self):
        logger.debug("Clearing screen")
        for widget in self.root.winfo_children():
            try:
                widget.destroy()
            except tk.TclError as e:
                logger.warning(f"Error destroying widget: {e}")
        for attr in ['parts_list_listbox', 'submit_button']:
            if hasattr(self, attr):
                delattr(self, attr)