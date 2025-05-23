# gui.py
# Purpose: Implements the graphical user interface (GUI) using Tkinter for the Sheet Metal Client Hub.
# Supports FR1 (Login), FR2 (Part Input), FR6 (Update Rates), FR7 (Generate Quote).
# Provides screens for login, part input, quote generation, and admin rate updates with a consistent footer.
# Integrates with calculator.py for cost calculations and file_handler.py for file operations.
# Uses messagebox for user feedback and logger.py for automatic test result logging.
# Designed for Python 3.9 with Tkinter, supporting 10 work centres, GBP, and mm units.

import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import os
import re
from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates
from calculator import calculate_cost
from logger import log_test_result
from PIL import Image, ImageTk

# Get the absolute path to the repository root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_existing_parts():
    """
    Load existing part IDs from data/output.txt for sub-parts dropdown.
    Returns a list of part IDs.
    """
    parts = []
    try:
        with open(os.path.join(BASE_DIR, 'data/output.txt'), 'r') as f:
            for line in f:
                if line.strip():
                    part_id = line.split(',')[0].strip()
                    if re.match(r"^PART-[A-Za-z0-9]{5,15}$", part_id):
                        parts.append(part_id)
        return parts
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading parts: {e}")
        return []

def load_parts_catalogue():
    """
    Load fasteners and PEM inserts from data/parts_catalogue.txt.
    Returns a list of tuples (item_id, description, price).
    """
    catalogue = []
    try:
        with open(os.path.join(BASE_DIR, 'data/parts_catalogue.txt'), 'r') as f:
            for line in f:
                if line.strip():
                    item_id, description, price = line.strip().split(',')
                    catalogue.append((item_id, description, float(price)))
        return catalogue
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error loading parts catalogue: {e}")
        return []

class SheetMetalClientHub:
    """
    Main GUI class for the Sheet Metal Client Hub application.
    Manages all screens (login, part input, quote, admin) and user interactions.
    """
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Parameters:
            root (tk.Tk): The Tkinter root window.
        
        Logic:
            1. Stores the root window.
            2. Sets the window title and fixed size to 1000x750 pixels.
            3. Sets a custom laser icon.
            4. Initializes role as None (set after login).
            5. Displays the login screen.
        """
        self.root = root
        self.root.title("Sheet Metal Client Hub")
        self.root.geometry("1000x750")
        self.root.resizable(False, False)  # Prevent resizing
        self.root.minsize(400, 400)  # Set minimum size as fallback
        # Set custom laser icon
        try:
            icon_path = os.path.join(BASE_DIR, 'docs/images/laser_gear.ico')
            self.root.iconbitmap(icon_path)
        except tk.TclError:
            print("Warning: Could not load laser_gear.ico, using default icon")
        self.role = None
        self.single_selected_sub_parts = []
        self.assembly_selected_sub_parts = []
        self.last_part_id = None
        self.last_total_cost = None
        self.create_login_screen()

    def create_footer(self, frame):
        """
        Create the footer for all screens with version and help button.
        
        Parameters:
            frame (tk.Frame): The footer frame to populate.
        
        Logic:
            1. Adds version label on the left.
            2. Adds help button on the right that opens a guide.
        """
        frame.configure(bg="lightgrey")
        tk.Label(frame, text="Version 1.0", font=("Arial", 10), bg="lightgrey").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(frame, text="Help", command=self.show_help, font=("Arial", 10), bg="lightgrey").pack(side=tk.RIGHT, padx=10, pady=5)

    def show_help(self):
        """
        Display a help guide for the application.
        
        Logic:
            1. Shows a messagebox with a placeholder guide.
            2. Logs the help action to data/test_logs.txt.
        """
        guide = (
            "Sheet Metal Client Hub - User Guide\n\n"
            "1. Login: Enter username and password (e.g., laurie:moffat123).\n"
            "2. Part Input: Enter part or assembly details, select fasteners/inserts or sub-parts, and WorkCentre operations.\n"
            "3. Quote: Generate a quote with customer name and profit margin.\n"
            "4. Admin: Update rates (e.g., mild_steel_rate) if admin.\n"
            "For support, contact [support email]."
        )
        messagebox.showinfo("Help - Sheet Metal Client Hub", guide)
        log_test_result(
            test_case="Help Guide Accessed",
            input_data="None",
            output="Help guide displayed",
            pass_fail="Pass"
        )

    def create_login_screen(self):
        """
        Create the login screen for user authentication (FR1).
        
        Logic:
            1. Clears existing widgets.
            2. Creates main content frame and footer.
            3. Adds title, username/password fields, login/clear buttons in main frame.
            4. Sets focus on username field and binds Enter key to login.
        """
        self.clear_screen()
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(main_frame, text="Login", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(main_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        self.username_entry.focus_set()
        tk.Label(main_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(main_frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(main_frame, text="Login", command=self.login, font=("Arial", 12)).grid(row=3, column=0, pady=10)
        tk.Button(main_frame, text="Clear", command=self.clear_login_fields, font=("Arial", 12)).grid(row=3, column=1, pady=10)
        self.root.bind('<Return>', lambda event: self.login())
        
        footer = tk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_footer(footer)

    def clear_login_fields(self):
        """
        Clear username and password entry fields.
        
        Logic:
            1. Deletes all text in username and password entries.
            2. Sets focus back to username field.
        """
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus_set()
        log_test_result(
            test_case="FR1: Clear login fields",
            input_data="None",
            output="Username and password fields cleared",
            pass_fail="Pass"
        )

    def login(self):
        """
        Handle login button click and validate credentials (FR1).
        
        Logic:
            1. Gets username and password from entry fields.
            2. Validates inputs (non-empty).
            3. Calls validate_credentials to check against data/users.txt.
            4. Sets role ("Admin" for username "admin", else "User").
            5. Logs test result to data/test_logs.txt using logger.
            6. Shows success message and navigates to appropriate screen.
            7. Shows and logs error message for invalid inputs or credentials.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            output = "Username and password cannot be empty"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR1: Login with empty fields",
                input_data=f"Username: {username}, Password: {password}",
                output=output,
                pass_fail="Fail"
            )
            return
        if validate_credentials(username, password):
            self.role = "Admin" if username == "admin" else "User"
            output = f"Login successful as {self.role}"
            messagebox.showinfo("Success", output)
            log_test_result(
                test_case=f"FR1: Valid {self.role} login",
                input_data=f"Username: {username}, Password: [hidden]",
                output=output,
                pass_fail="Pass"
            )
            if self.role == "User":
                self.create_part_input_screen()
            else:
                self.create_admin_screen()
        else:
            output = "Invalid username or password"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR1: Invalid login",
                input_data=f"Username: {username}, Password: [hidden]",
                output=output,
                pass_fail="Fail"
            )

    def prompt_admin_credentials(self):
        """
        Prompt for admin credentials in a dialog window.
        Returns True if valid, False otherwise.
        """
        dialog = Toplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Admin Username:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        admin_username_entry = tk.Entry(dialog, font=("Arial", 12))
        admin_username_entry.grid(row=0, column=1, padx=10, pady=5)
        admin_username_entry.focus_set()

        tk.Label(dialog, text="Admin Password:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        admin_password_entry = tk.Entry(dialog, show="*", font=("Arial", 12))
        admin_password_entry.grid(row=1, column=1, padx=10, pady=5)

        result = {"valid": False}

        def validate():
            username = admin_username_entry.get().strip()
            password = admin_password_entry.get().strip()
            if not username or not password:
                messagebox.showerror("Error", "Username and password cannot be empty", parent=dialog)
                log_test_result(
                    test_case="Admin Credential Prompt: Empty fields",
                    input_data=f"Username: {username}, Password: [hidden]",
                    output="Username and password cannot be empty",
                    pass_fail="Fail"
                )
                return
            if validate_credentials(username, password) and username == "admin":
                result["valid"] = True
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Invalid admin credentials", parent=dialog)
                log_test_result(
                    test_case="Admin Credential Prompt: Invalid credentials",
                    input_data=f"Username: {username}, Password: [hidden]",
                    output="Invalid admin credentials",
                    pass_fail="Fail"
                )

        tk.Button(dialog, text="Submit", command=validate, font=("Arial", 12)).grid(row=2, column=0, pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, font=("Arial", 12)).grid(row=2, column=1, pady=10)
        dialog.bind('<Return>', lambda event: validate())

        self.root.wait_window(dialog)
        return result["valid"]

    def update_quantity_entry_state(self):
        """
        Enable or disable the custom quantity entry based on the quantity dropdown selection.
        """
        if self.assembly_quantity_var.get() == "Other":
            self.assembly_custom_quantity_entry.config(state='normal')
        else:
            self.assembly_custom_quantity_entry.config(state='disabled')

    def update_sub_parts_dropdown(self, tab_index):
        """
        Update the sub-parts dropdown based on tab selection.
        - Assembly (tab_index=1): Load existing parts from data/output.txt.
        - Single Part (tab_index=0): Load fasteners/inserts from data/parts_catalogue.txt.
        """
        if tab_index == 0:
            var = self.single_sub_parts_var
            option = self.single_sub_parts_option
        else:
            var = self.assembly_sub_parts_var
            option = self.assembly_sub_parts_option

        var.set("Select Item")
        menu = option['menu']
        menu.delete(0, tk.END)
        menu.add_command(label="Select Item", command=lambda: var.set("Select Item"))
        
        if tab_index == 1:  # Assembly
            existing_parts = load_existing_parts()
            if existing_parts:
                for part_id in existing_parts:
                    menu.add_command(label=part_id, command=lambda x=part_id: var.set(x))
            else:
                menu.add_command(label="No parts available", command=lambda: var.set("No parts available"))
        else:  # Single Part
            catalogue = load_parts_catalogue()
            if catalogue:
                for item_id, description, _ in catalogue:
                    label = f"{item_id}: {description}"
                    menu.add_command(label=label, command=lambda x=label: var.set(x))
            else:
                menu.add_command(label="No catalogue items available", command=lambda: var.set("No catalogue items available"))

    def add_sub_part(self, tab_index):
        """
        Add the selected sub-part or fastener to the list of selected items.
        """
        if tab_index == 0:
            selected_item = self.single_sub_parts_var.get()
            selected_list = self.single_selected_sub_parts
            label = self.single_selected_sub_parts_label
        else:
            selected_item = self.assembly_sub_parts_var.get()
            selected_list = self.assembly_selected_sub_parts
            label = self.assembly_selected_sub_parts_label

        if selected_item and selected_item not in ["Select Item", "No parts available", "No catalogue items available"]:
            if selected_item not in selected_list:
                selected_list.append(selected_item)
                label.config(text=f"Selected Items: {', '.join(selected_list)}")
            if tab_index == 0:
                self.single_sub_parts_var.set("Select Item")
            else:
                self.assembly_sub_parts_var.set("Select Item")

    def clear_sub_parts(self, tab_index):
        """
        Clear all selected sub-parts or fasteners and update the display.
        """
        if tab_index == 0:
            self.single_selected_sub_parts = []
            self.single_selected_sub_parts_label.config(text="Selected Items: None")
        else:
            self.assembly_selected_sub_parts = []
            self.assembly_selected_sub_parts_label.config(text="Selected Items: None")

    def go_to_settings(self):
        """
        Navigate to admin settings screen, prompting for credentials if not admin.
        """
        if self.role == "Admin":
            self.create_admin_screen()
        elif self.prompt_admin_credentials():
            self.role = "Admin"
            self.create_admin_screen()
        else:
            messagebox.showerror("Error", "Admin access denied")
            log_test_result(
                test_case="Settings Access: Denied",
                input_data="Non-admin user",
                output="Admin access denied",
                pass_fail="Fail"
            )

    def go_back_to_login(self):
        """
        Return to the login screen and reset role.
        """
        self.role = None
        self.create_login_screen()
        log_test_result(
            test_case="Back to Login",
            input_data="None",
            output="Returned to login screen",
            pass_fail="Pass"
        )

    def reset_part_input(self):
        """
        Reset all part input fields to default values.
        """
        self.part_id_entry.delete(0, tk.END)
        self.revision_entry.delete(0, tk.END)
        self.notebook.select(0)
        self.single_material_var.set("Mild Steel")
        self.single_thickness_var.set("1.0")
        self.single_lay_flat_length_var.set("1000")
        self.single_lay_flat_width_var.set("500")
        self.single_weldment_var.set("No")
        self.single_selected_sub_parts = []
        self.single_selected_sub_parts_label.config(text="Selected Items: None")
        self.single_sub_parts_var.set("Select Item")
        self.assembly_quantity_var.set("1")
        self.assembly_custom_quantity_entry.delete(0, tk.END)
        self.assembly_custom_quantity_entry.config(state='disabled')
        self.assembly_selected_sub_parts = []
        self.assembly_selected_sub_parts_label.config(text="Selected Items: None")
        self.assembly_sub_parts_var.set("Select Item")
        for var in self.work_centre_vars:
            var.set("None")
        self.submit_button.config(state='disabled')
        self.add_another_part_button.config(state='disabled')
        log_test_result(
            test_case="Reset Part Input",
            input_data="None",
            output="All fields reset to default",
            pass_fail="Pass"
        )

    def create_part_input_screen(self):
        """
        Create the part input screen for entering part specifications (FR2).
        
        Logic:
            1. Clears existing widgets.
            2. Creates top frame for overarching title and image.
            3. Creates main content frame with a vertical split (left: part inputs, right: Planned Operations).
            4. Left side: Tabbed interface for Single Part/Assembly, right-aligned near centerline.
            5. Right side: Planned Operations with 10 operations, Calculate Cost/Submit/Add Another Part buttons.
            6. Bottom frame: Settings, Back buttons.
            7. Adds a centered vertical line and footer.
        """
        self.clear_screen()

        # Top frame for title and image
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Load and display laser_gear image
        try:
            image_path = os.path.join(BASE_DIR, 'docs/images/laser_gear.png')
            image = Image.open(image_path).resize((32, 32), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(top_frame, image=photo)
            image_label.image = photo  # Keep reference
            image_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading laser_gear image: {e}")
            tk.Label(top_frame, text="[Laser Gear Image]", font=("Arial", 10)).pack(pady=5)

        tk.Label(top_frame, text="Manufacturing Input Screen", font=("Arial", 16, "bold")).pack(pady=5)

        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)

        # Left frame
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Separator
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.grid(row=0, column=1, sticky="ns")

        # Right frame
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=2, sticky="nsew")

        # Input frame in left frame
        input_frame = tk.Frame(left_frame)
        input_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Planned Materials title
        tk.Label(input_frame, text="Planned Materials", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Common fields
        self.part_id_label = tk.Label(input_frame, text="Part ID:", font=("Arial", 12))
        self.part_id_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.revision_label = tk.Label(input_frame, text="Revision:", font=("Arial", 12))
        self.revision_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.part_id_label.grid(row=1, column=0, sticky="e", padx=(10, 2), pady=2)
        self.part_id_entry.grid(row=1, column=1, sticky="w", padx=(2, 5), pady=2)
        self.revision_label.grid(row=2, column=0, sticky="e", padx=(10, 2), pady=2)
        self.revision_entry.grid(row=2, column=1, sticky="w", padx=(2, 5), pady=2)

        # Notebook for tabs
        self.notebook = ttk.Notebook(input_frame)
        self.notebook.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)

        # Single Part tab
        self.single_part_frame = tk.Frame(self.notebook)
        self.notebook.add(self.single_part_frame, text="Single Part")

        self.single_material_label = tk.Label(self.single_part_frame, text="Material:", font=("Arial", 12))
        self.single_material_var = tk.StringVar(value="Mild Steel")
        self.single_material_option = tk.OptionMenu(self.single_part_frame, self.single_material_var, "Mild Steel", "Aluminium", "Stainless Steel")
        self.single_thickness_label = tk.Label(self.single_part_frame, text="Thickness (mm):", font=("Arial", 12))
        self.single_thickness_var = tk.StringVar(value="1.0")
        self.single_thickness_option = tk.OptionMenu(self.single_part_frame, self.single_thickness_var, "1.0", "1.2", "1.5", "2.0", "2.5", "3.0")
        self.single_lay_flat_length_label = tk.Label(self.single_part_frame, text="Lay-Flat Length (mm):", font=("Arial", 12))
        self.single_lay_flat_length_var = tk.StringVar(value="1000")
        self.single_lay_flat_length_option = tk.OptionMenu(self.single_part_frame, self.single_lay_flat_length_var, "50", "100", "500", "1000", "1500", "2000", "3000")
        self.single_lay_flat_width_label = tk.Label(self.single_part_frame, text="Lay-Flat Width (mm):", font=("Arial", 12))
        self.single_lay_flat_width_var = tk.StringVar(value="500")
        self.single_lay_flat_width_option = tk.OptionMenu(self.single_part_frame, self.single_lay_flat_width_var, "50", "100", "500", "1000", "1500")
        self.single_weldment_label = tk.Label(self.single_part_frame, text="Weldment Indicator:", font=("Arial", 12))
        self.single_weldment_var = tk.StringVar(value="No")
        self.single_weldment_option = tk.OptionMenu(self.single_part_frame, self.single_weldment_var, "Yes", "No")
        self.single_sub_parts_label = tk.Label(self.single_part_frame, text="Fasteners/Inserts:", font=("Arial", 12))
        self.single_sub_parts_var = tk.StringVar(value="Select Item")
        self.single_sub_parts_option = tk.OptionMenu(self.single_part_frame, self.single_sub_parts_var, "Select Item")
        self.single_add_sub_part_button = tk.Button(self.single_part_frame, text="Add Fastener/Insert", command=lambda: self.add_sub_part(0), font=("Arial", 12))
        self.single_clear_sub_parts_button = tk.Button(self.single_part_frame, text="Clear Selected", command=lambda: self.clear_sub_parts(0), font=("Arial", 12))
        self.single_selected_sub_parts_label = tk.Label(self.single_part_frame, text="Selected Items: None", font=("Arial", 12), wraplength=400, justify="left")

        self.single_material_label.grid(row=0, column=0, sticky="e", padx=(10, 2), pady=2)
        self.single_material_option.grid(row=0, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_thickness_label.grid(row=1, column=0, sticky="e", padx=(10, 2), pady=2)
        self.single_thickness_option.grid(row=1, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_lay_flat_length_label.grid(row=2, column=0, sticky="e", padx=(10, 2), pady=2)
        self.single_lay_flat_length_option.grid(row=2, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_lay_flat_width_label.grid(row=3, column=0, sticky="e", padx=(10, 2), pady=2)
        self.single_lay_flat_width_option.grid(row=3, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_weldment_label.grid(row=4, column=0, sticky="e", padx=(10, 2), pady=2)
        self.single_weldment_option.grid(row=4, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_sub_parts_label.grid(row=5, column=0, sticky="e", padx=(10, 2), pady=2)
        self.single_sub_parts_option.grid(row=5, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_add_sub_part_button.grid(row=6, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_clear_sub_parts_button.grid(row=7, column=1, sticky="w", padx=(2, 5), pady=2)
        self.single_selected_sub_parts_label.grid(row=8, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=2)

        # Assembly tab
        self.assembly_part_frame = tk.Frame(self.notebook)
        self.notebook.add(self.assembly_part_frame, text="Assembly")

        self.assembly_quantity_label = tk.Label(self.assembly_part_frame, text="Quantity:", font=("Arial", 12))
        self.assembly_quantity_var = tk.StringVar(value="1")
        self.assembly_quantity_option = tk.OptionMenu(self.assembly_part_frame, self.assembly_quantity_var, "1", "5", "10", "20", "50", "100", "Other")
        self.assembly_custom_quantity_entry = tk.Entry(self.assembly_part_frame, font=("Arial", 12), state='disabled')
        self.assembly_sub_parts_label = tk.Label(self.assembly_part_frame, text="Sub-Parts:", font=("Arial", 12))
        self.assembly_sub_parts_var = tk.StringVar(value="Select Item")
        self.assembly_sub_parts_option = tk.OptionMenu(self.assembly_part_frame, self.assembly_sub_parts_var, "Select Item")
        self.assembly_add_sub_part_button = tk.Button(self.assembly_part_frame, text="Add Sub-Part", command=lambda: self.add_sub_part(1), font=("Arial", 12))
        self.assembly_clear_sub_parts_button = tk.Button(self.assembly_part_frame, text="Clear Selected", command=lambda: self.clear_sub_parts(1), font=("Arial", 12))
        self.assembly_selected_sub_parts_label = tk.Label(self.assembly_part_frame, text="Selected Items: None", font=("Arial", 12), wraplength=400, justify="left")

        self.assembly_quantity_label.grid(row=0, column=0, sticky="e", padx=(10, 2), pady=2)
        self.assembly_quantity_option.grid(row=0, column=1, sticky="w", padx=(2, 5), pady=2)
        self.assembly_custom_quantity_entry.grid(row=1, column=1, sticky="w", padx=(2, 5), pady=2)
        self.assembly_sub_parts_label.grid(row=2, column=0, sticky="e", padx=(10, 2), pady=2)
        self.assembly_sub_parts_option.grid(row=2, column=1, sticky="w", padx=(2, 5), pady=2)
        self.assembly_add_sub_part_button.grid(row=3, column=1, sticky="w", padx=(2, 5), pady=2)
        self.assembly_clear_sub_parts_button.grid(row=4, column=1, sticky="w", padx=(2, 5), pady=2)
        self.assembly_selected_sub_parts_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=(10, 5), pady=2)

        self.assembly_quantity_var.trace("w", lambda *args: self.update_quantity_entry_state())

        # Operations frame in right frame
        operations_frame = tk.Frame(right_frame)
        operations_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(operations_frame, text="Planned Operations", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # WorkCentre options
        work_centres = [
            "Cutting", "Bending", "Welding", "Assembly", "Finishing",
            "Drilling", "Punching", "Grinding", "Coating", "Inspection"
        ]
        self.work_centre_vars = []
        for i in range(10):  # Operations 10 to 100
            op_label = f"Operation {(i+1)*10}:"
            tk.Label(operations_frame, text=op_label, font=("Arial", 10)).grid(row=i+1, column=0, sticky="w", padx=(5, 2), pady=2)
            var = tk.StringVar(value="None")
            tk.OptionMenu(operations_frame, var, "None", *work_centres).grid(row=i+1, column=1, sticky="w", padx=(2, 5), pady=2)
            self.work_centre_vars.append(var)

        # Calculate Cost and buttons subframe
        self.calculate_cost_button = tk.Button(operations_frame, text="Calculate Cost", command=self.calculate_and_save, font=("Arial", 10))
        self.calculate_cost_button.grid(row=11, column=0, columnspan=2, pady=5)

        buttons_subframe = tk.Frame(operations_frame)
        buttons_subframe.grid(row=12, column=0, columnspan=2, pady=5)

        self.submit_button = tk.Button(buttons_subframe, text="Submit", command=lambda: self.create_quote_screen(self.last_part_id, self.last_total_cost), font=("Arial", 10), state='disabled')
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.add_another_part_button = tk.Button(buttons_subframe, text="Add Another Part", command=self.reset_part_input, font=("Arial", 10), state='disabled')
        self.add_another_part_button.pack(side=tk.LEFT, padx=5)

        # Bottom frame for navigation buttons
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)

        self.settings_button = tk.Button(bottom_frame, text="Settings", command=self.go_to_settings, font=("Arial", 12))
        self.back_button = tk.Button(bottom_frame, text="Back", command=self.go_back_to_login, font=("Arial", 12))
        self.settings_button.pack(side=tk.LEFT, padx=10)
        self.back_button.pack(side=tk.LEFT, padx=10)

        # Footer
        footer = tk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_footer(footer)

        # Initialize sub-parts dropdowns
        self.update_sub_parts_dropdown(0)
        self.update_sub_parts_dropdown(1)

    def on_tab_changed(self, event):
        """
        Handle tab change event to update sub-parts dropdown.
        """
        selected_tab = self.notebook.index(self.notebook.select())
        self.update_sub_parts_dropdown(selected_tab)

    def calculate_and_save(self):
        """
        Calculate cost and save output based on part specifications (FR2, FR3, FR4, FR5).
        
        Logic:
            1. Retrieves part specifications based on selected tab.
            2. Validates inputs, including WorkCentre operations.
            3. Calculates cost including catalogue items and WorkCentres.
            4. Saves result and enables Submit/Add Another Part buttons.
        """
        try:
            selected_tab = self.notebook.index(self.notebook.select())
            part_type = "Single Part" if selected_tab == 0 else "Assembly"
            part_id = self.part_id_entry.get().strip()
            revision = self.revision_entry.get().strip()
            work_centres = [var.get() for var in self.work_centre_vars if var.get() != "None"]

            if selected_tab == 0:  # Single Part
                material = self.single_material_var.get().lower()
                thickness = self.single_thickness_var.get()
                length = self.single_lay_flat_length_var.get()
                width = self.single_lay_flat_width_var.get()
                weldment_indicator = self.single_weldment_var.get()
                sub_parts = self.single_selected_sub_parts
                quantity = "1"
                top_level_assembly = "N/A"
            else:  # Assembly
                material = "N/A"
                thickness = "0.0"
                length = "0"
                width = "0"
                weldment_indicator = "No"
                quantity = self.assembly_quantity_var.get()
                if quantity == "Other":
                    quantity = self.assembly_custom_quantity_entry.get().strip()
                sub_parts = self.assembly_selected_sub_parts
                top_level_assembly = part_id

            input_data = (f"Part Type: {part_type}, Part ID: {part_id}, Revision: {revision}, Material: {material}, "
                          f"Thickness: {thickness}, Length: {length}, Width: {width}, Quantity: {quantity}, "
                          f"Sub-Parts: {sub_parts}, Weldment: {weldment_indicator}, Top-Level Assembly: {top_level_assembly}, "
                          f"Work Centres: {work_centres}")

            if not all([part_id, revision]):
                output = "Part ID and Revision are required"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR2: Part input with empty fields",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return

            if part_type == "Assembly":
                if not quantity:
                    output = "Quantity is required for assemblies"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Assembly with no quantity",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
                if not sub_parts:
                    output = "At least one sub-part must be selected for an assembly"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Assembly with no sub-parts",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
            else:  # Single Part
                if not all([material, thickness, length, width]):
                    output = "Material, Thickness, Lay-Flat Length, and Width are required for single parts"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Single part with empty fields",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return

            if not work_centres:
                output = "At least one WorkCentre operation must be selected"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR2: No WorkCentre operations selected",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return

            thickness = float(thickness) if part_type == "Single Part" else 0.0
            length = int(length) if part_type == "Single Part" else 0
            width = int(width) if part_type == "Single Part" else 0
            quantity = int(quantity) if part_type == "Assembly" else 1

            if not re.match(r"^PART-[A-Za-z0-9]{5,15}$", part_id):
                output = "Part ID must be PART-[5-15 alphanumeric]"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR2: Invalid part ID",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return
            if part_type == "Single Part":
                if material not in ['mild steel', 'aluminium', 'stainless steel']:
                    output = "Material must be 'Mild Steel', 'Aluminium', or 'Stainless Steel'"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Invalid material",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
                if not (1.0 <= thickness <= 3.0):
                    output = "Thickness must be between 1.0 and 3.0 mm"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Invalid thickness",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
                if not (50 <= length <= 3000):
                    output = "Lay-Flat length must be between 50 and 3000 mm"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Invalid lay-flat length",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
                if not (50 <= width <= 1500):
                    output = "Lay-Flat width must be between 50 and 1500 mm"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Invalid lay-flat width",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
            if part_type == "Assembly" and quantity <= 0:
                output = "Quantity must be a positive integer"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR2: Invalid quantity",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return
            if part_type == "Assembly":
                for sub_part in sub_parts:
                    if sub_part not in load_existing_parts():
                        output = f"Sub-part {sub_part} does not exist in the system"
                        messagebox.showerror("Error", output)
                        log_test_result(
                            test_case="FR2: Invalid sub-part",
                            input_data=input_data,
                            output=output,
                            pass_fail="Fail"
                        )
                        return

            # Calculate catalogue cost for single parts
            catalogue_cost = 0.0
            if part_type == "Single Part":
                catalogue = load_parts_catalogue()
                for item_id in sub_parts:
                    item_id = item_id.split(':')[0].strip()  # Extract item_id
                    for cat_id, _, price in catalogue:
                        if item_id == cat_id:
                            catalogue_cost += price
                            break

            part_specs = {
                'part_type': part_type,
                'part_id': part_id,
                'revision': revision,
                'material': material,
                'thickness': thickness,
                'length': length,
                'width': width,
                'quantity': quantity,
                'sub_parts': sub_parts,
                'top_level_assembly': top_level_assembly,
                'weldment_indicator': weldment_indicator,
                'catalogue_cost': catalogue_cost,
                'work_centres': work_centres
            }

            rates = load_rates()
            if not rates:
                output = "Failed to load rates from data/rates_global.txt"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR3: Cost calculation with missing rates",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return

            total_cost = calculate_cost(part_specs, rates)
            if total_cost == 0.0:
                output = "Cost calculation failed, check inputs or rates"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR3-FR4: Cost calculation failure",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return

            save_output(part_id, revision, material, thickness, length, width, quantity, total_cost)
            output = f"Cost calculated: £{total_cost}\nSaved to data/output.txt"
            messagebox.showinfo("Success", output)
            log_test_result(
                test_case="FR3-FR4-FR5: Cost calculation and output storage",
                input_data=input_data,
                output=output,
                pass_fail="Pass"
            )
            self.submit_button.config(state='normal')
            self.add_another_part_button.config(state='normal')
            self.last_part_id = part_id
            self.last_total_cost = total_cost
        except ValueError:
            output = "Invalid input: Quantity must be valid"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR2: Invalid numeric input",
                input_data=input_data,
                output=output,
                pass_fail="Fail"
            )
        except Exception as e:
            output = f"Unexpected error: {e}"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR2-FR3-FR4: Unexpected error",
                input_data=input_data,
                output=output,
                pass_fail="Fail"
            )

    def create_quote_screen(self, part_id, total_cost):
        """
        Create the quote generation screen (FR7).
        
        Parameters:
            part_id (str): Part identifier.
            total_cost (float): Calculated cost from calculate_cost.
        
        Logic:
            1. Clears existing widgets.
            2. Creates main content frame and footer.
            3. Adds fields for customer name and profit margin, and generate quote button.
        """
        self.clear_screen()
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(main_frame, text="Generate Quote", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(main_frame, text="Customer Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.customer_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.customer_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(main_frame, text="Profit Margin (%):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.margin_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.margin_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(main_frame, text="Generate Quote", command=lambda: self.generate_quote(part_id, total_cost), font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=10)
        
        footer = tk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_footer(footer)

    def generate_quote(self, part_id, total_cost):
        """
        Generate and save a quote (FR7).
        
        Logic:
            1. Retrieves customer name and profit margin from entry fields.
            2. Validates inputs (non-empty customer name, numeric non-negative margin).
            3. Calls save_quote to generate and save the quote to data/quotes.txt.
            4. Logs test result to data/test_logs.txt using logger.
            5. Shows success message.
            6. Returns to part input screen.
        """
        try:
            customer_name = self.customer_entry.get().strip()
            profit_margin = self.margin_entry.get().strip()
            input_data = f"Customer Name: {customer_name}, Profit Margin: {profit_margin}%"
            
            if not customer_name:
                output = "Customer name cannot be empty"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR7: Quote with empty customer name",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return
            
            profit_margin = float(profit_margin)
            if profit_margin < 0:
                output = "Profit margin cannot be negative"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR7: Quote with negative margin",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return

            save_quote(part_id, total_cost, customer_name, profit_margin)
            output = "Quote generated and saved to data/quotes.txt"
            messagebox.showinfo("Success", output)
            log_test_result(
                test_case="FR7: Generate quote",
                input_data=input_data,
                output=output,
                pass_fail="Pass"
            )
            self.create_part_input_screen()
        except ValueError:
            output = "Invalid profit margin: please enter a numeric value"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR7: Quote with invalid margin",
                input_data=input_data,
                output=output,
                pass_fail="Fail"
            )
        except Exception as e:
            output = f"Unexpected error: {e}"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR7: Unexpected error",
                input_data=input_data,
                output=output,
                pass_fail="Fail"
            )

    def create_admin_screen(self):
        """
        Create the admin screen for updating rates (FR6).
        
        Logic:
            1. Clears existing widgets.
            2. Creates main content frame and footer.
            3. Adds fields for rate key and value, update rate button, and user features button.
        """
        self.clear_screen()
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(main_frame, text="Admin Settings", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(main_frame, text="Rate Key (e.g., mild_steel_rate):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.rate_key_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.rate_key_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(main_frame, text="Rate Value (GBP):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.rate_value_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.rate_value_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(main_frame, text="Update Rate", command=self.update_rate, font=("Arial", 12)).grid(row=3, column=0, pady=10)
        tk.Button(main_frame, text="User Features", command=self.create_part_input_screen, font=("Arial", 12)).grid(row=3, column=1, pady=10)
        
        footer = tk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_footer(footer)

    def update_rate(self):
        """
        Update a rate in data/rates_global.txt (FR6).
        
        Logic:
            1. Retrieves rate key and value from entry fields.
            2. Validates inputs (non-empty key, numeric non-negative value).
            3. Calls update_rates to save the new rate.
            4. Logs test result to data/test_logs.txt using logger.
            5. Shows success message.
        """
        try:
            rate_key = self.rate_key_entry.get().strip()
            rate_value = self.rate_value_entry.get().strip()
            input_data = f"Rate Key: {rate_key}, Rate Value: {rate_value}"
            
            if not rate_key:
                output = "Rate key cannot be empty"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR6: Update rate with empty key",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return
            
            rate_value = float(rate_value)
            if rate_value < 0:
                output = "Rate value cannot be negative"
                messagebox.showerror("Error", output)
                log_test_result(
                    test_case="FR6: Update rate with negative value",
                    input_data=input_data,
                    output=output,
                    pass_fail="Fail"
                )
                return
            
            update_rates(rate_key, rate_value)
            output = f"Rate '{rate_key}' updated to {rate_value} in data/rates_global.txt"
            messagebox.showinfo("Success", output)
            log_test_result(
                test_case="FR6: Update rate",
                input_data=input_data,
                output=output,
                pass_fail="Pass"
            )
        except ValueError:
            output = "Invalid rate value: please enter a numeric value"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR6: Update rate with invalid value",
                input_data=input_data,
                output=output,
                pass_fail="Fail"
            )
        except Exception as e:
            output = f"Unexpected error: {e}"
            messagebox.showerror("Error", output)
            log_test_result(
                test_case="FR6: Unexpected error",
                input_data=input_data,
                output=output,
                pass_fail="Fail"
            )

    def clear_screen(self):
        """
        Clear all widgets from the current screen.
        
        Logic:
            1. Destroys all child widgets of the root window.
            2. Used to switch between screens (e.g., login to part input).
        """
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SheetMetalClientHub(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        log_test_result(
            test_case="GUI Initialization",
            input_data="None",
            output=f"Error starting GUI: {e}",
            pass_fail="Fail"
        )
