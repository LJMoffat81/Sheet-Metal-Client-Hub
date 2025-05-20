# gui.py
# Purpose: Implements the graphical user interface (GUI) using Tkinter for the Sheet Metal Client Hub.
# Supports FR1 (Login), FR2 (Part Input), FR6 (Update Rates), FR7 (Generate Quote).
# Provides screens for login, part input, quote generation, and admin rate updates with a consistent footer.
# Integrates with calculator.py for cost calculations and file_handler.py for file operations.
# Uses messagebox for user feedback and logger.py for automatic test result logging.
# Designed for Python 3.9 with Tkinter, supporting 10 work centres, GBP, and mm units.

import tkinter as tk
from tkinter import messagebox
import os
import re
from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates
from calculator import calculate_cost
from logger import log_test_result

# Get the absolute path to the repository root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_existing_parts():
    """
    Load existing part IDs from output.txt for sub-parts dropdown.
    Returns a list of part IDs.
    """
    parts = []
    try:
        with open(os.path.join(BASE_DIR, 'output.txt'), 'r') as f:
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
    Load fasteners and PEM inserts from parts_catalogue.txt.
    Returns a list of tuples (item_id, description, price).
    """
    catalogue = []
    try:
        with open(os.path.join(BASE_DIR, 'parts_catalogue.txt'), 'r') as f:
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
            2. Logs the help action to test_logs.txt.
        """
        guide = (
            "Sheet Metal Client Hub - User Guide\n\n"
            "1. Login: Enter username and password (e.g., laurie:moffat123).\n"
            "2. Part Input: Enter part or assembly details, select fasteners/inserts or sub-parts.\n"
            "3. Quote: Generate a quote with customer name and profit margin.\n"
            "4. Admin: Update rates (e.g., steel_rate) if admin.\n"
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
            3. Calls validate_credentials to check against users.txt.
            4. Sets role ("Admin" for username "admin", else "User").
            5. Logs test result to test_logs.txt using logger.
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

    def update_quantity_entry_state(self):
        """
        Enable or disable the custom quantity entry based on the quantity dropdown selection.
        Logic:
            1. If "Other" is selected, enable the custom quantity entry.
            2. Otherwise, disable it.
        """
        if hasattr(self, 'custom_quantity_entry') and self.quantity_var.get() == "Other":
            self.custom_quantity_entry.config(state='normal')
        elif hasattr(self, 'custom_quantity_entry'):
            self.custom_quantity_entry.config(state='disabled')

    def update_part_input_fields(self, *args):
        """
        Show or hide fields based on part type selection.
        Logic:
            - Assembly: Show Part ID, Revision, Quantity, Sub-Parts.
            - Single Part: Show Part ID, Revision, Material, Thickness, Lay-Flat, Weldment, Fasteners/Inserts.
        """
        part_type = self.part_type_var.get()
        
        # Hide all fields initially
        for widget in [self.part_id_label, self.part_id_entry,
                       self.revision_label, self.revision_entry,
                       self.material_label, self.material_option,
                       self.thickness_label, self.thickness_option,
                       self.lay_flat_label, self.lay_flat_entry,
                       self.quantity_label, self.quantity_option, self.custom_quantity_entry,
                       self.sub_parts_label, self.sub_parts_listbox,
                       self.weldment_label, self.weldment_option]:
            widget.grid_remove()
        
        # Show common fields
        self.part_id_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.part_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.revision_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.revision_entry.grid(row=2, column=1, padx=5, pady=5)
        
        if part_type == "Assembly":
            self.quantity_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.quantity_option.grid(row=3, column=1, padx=5, pady=5, sticky="w")
            self.custom_quantity_entry.grid(row=3, column=1, padx=5, pady=5, sticky="e")
            self.sub_parts_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
            self.sub_parts_listbox.grid(row=4, column=1, padx=5, pady=5)
        else:  # Single Part
            self.material_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.material_option.grid(row=3, column=1, padx=5, pady=5, sticky="w")
            self.thickness_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
            self.thickness_option.grid(row=4, column=1, padx=5, pady=5, sticky="w")
            self.lay_flat_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
            self.lay_flat_entry.grid(row=5, column=1, padx=5, pady=5)
            self.weldment_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
            self.weldment_option.grid(row=6, column=1, padx=5, pady=5, sticky="w")
            self.sub_parts_label.grid(row=7, column=0, padx=5, pady=5, sticky="e")
            self.sub_parts_listbox.grid(row=7, column=1, padx=5, pady=5)

    def create_part_input_screen(self):
        """
        Create the part input screen for entering part specifications (FR2).
        
        Logic:
            1. Clears existing widgets.
            2. Creates main content frame with a vertical split (left: part inputs, right: BOM route card).
            3. Left side: Conditional fields based on part type (Assembly or Single Part).
            4. Right side: BOM route card (hidden for now).
            5. Adds a central vertical line and footer.
        """
        self.clear_screen()
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left side: Part input data
        left_frame = tk.Frame(main_frame, width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        tk.Label(left_frame, text="Part Input", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Part Type
        tk.Label(left_frame, text="Part Type:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.part_type_var = tk.StringVar(value="Single Part")
        self.part_type_var.trace("w", self.update_part_input_fields)
        tk.OptionMenu(left_frame, self.part_type_var, "Single Part", "Assembly").grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Initialize all fields (will be shown/hidden by update_part_input_fields)
        self.part_id_label = tk.Label(left_frame, text="Part ID:", font=("Arial", 12))
        self.part_id_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.revision_label = tk.Label(left_frame, text="Revision:", font=("Arial", 12))
        self.revision_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.material_label = tk.Label(left_frame, text="Material:", font=("Arial", 12))
        self.material_var = tk.StringVar(value="steel")
        self.material_option = tk.OptionMenu(left_frame, self.material_var, "steel", "aluminum")
        self.thickness_label = tk.Label(left_frame, text="Thickness (mm):", font=("Arial", 12))
        self.thickness_var = tk.StringVar(value="1.0")
        self.thickness_option = tk.OptionMenu(left_frame, self.thickness_var, "1.0", "1.2", "1.5", "2.0", "2.5", "3.0")
        self.lay_flat_label = tk.Label(left_frame, text="Lay-Flat (LxW mm):", font=("Arial", 12))
        self.lay_flat_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.quantity_label = tk.Label(left_frame, text="Quantity:", font=("Arial", 12))
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_var.trace("w", lambda *args: self.update_quantity_entry_state())
        self.quantity_option = tk.OptionMenu(left_frame, self.quantity_var, "1", "5", "10", "20", "50", "100", "Other")
        self.custom_quantity_entry = tk.Entry(left_frame, font=("Arial", 12), state='disabled')
        self.sub_parts_label = tk.Label(left_frame, text="Sub-Parts/Fasteners:", font=("Arial", 12))
        self.sub_parts_listbox = tk.Listbox(left_frame, selectmode='multiple', height=5, width=30, font=("Arial", 12))
        self.weldment_label = tk.Label(left_frame, text="Weldment Indicator:", font=("Arial", 12))
        self.weldment_var = tk.StringVar(value="No")
        self.weldment_option = tk.OptionMenu(left_frame, self.weldment_var, "Yes", "No")

        # Populate sub-parts listbox based on part type
        self.update_part_input_fields()
        self.part_type_var.set("Single Part")  # Trigger initial update
        self.update_sub_parts_listbox()

        # Central vertical line
        separator = tk.Canvas(main_frame, width=2, bg="black")
        separator.pack(side=tk.LEFT, fill=tk.Y)

        # Right side: BOM route card (hidden for now)
        right_frame = tk.Frame(main_frame, width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        tk.Label(right_frame, text="BOM Route Card", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Calculate Cost button
        tk.Button(main_frame, text="Calculate Cost", command=self.calculate_and_save, font=("Arial", 12)).pack(pady=10)

        # Footer
        footer = tk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_footer(footer)

    def update_sub_parts_listbox(self):
        """
        Update the sub-parts listbox based on part type.
        - Assembly: Load existing parts from output.txt.
        - Single Part: Load fasteners/inserts from parts_catalogue.txt.
        """
        self.sub_parts_listbox.delete(0, tk.END)
        if self.part_type_var.get() == "Assembly":
            existing_parts = load_existing_parts()
            if existing_parts:
                for part_id in existing_parts:
                    self.sub_parts_listbox.insert(tk.END, part_id)
            else:
                self.sub_parts_listbox.insert(tk.END, "No parts available")
        else:  # Single Part
            catalogue = load_parts_catalogue()
            if catalogue:
                for item_id, description, _ in catalogue:
                    self.sub_parts_listbox.insert(tk.END, f"{item_id}: {description}")
            else:
                self.sub_parts_listbox.insert(tk.END, "No catalogue items available")

    def calculate_and_save(self):
        """
        Calculate cost and save output based on part specifications (FR2, FR3, FR4, FR5).
        
        Logic:
            1. Retrieves part specifications based on part type.
            2. Validates inputs.
            3. Calculates cost including catalogue items for single parts.
            4. Saves result and navigates to quote screen.
        """
        try:
            part_type = self.part_type_var.get()
            part_id = self.part_id_entry.get().strip()
            revision = self.revision_entry.get().strip()
            material = self.material_var.get().lower() if part_type == "Single Part" else "N/A"
            thickness = self.thickness_var.get() if part_type == "Single Part" else "0.0"
            lay_flat = self.lay_flat_entry.get().strip() if part_type == "Single Part" else "0x0"
            quantity = self.quantity_var.get() if part_type == "Assembly" else "1"
            if quantity == "Other":
                quantity = self.custom_quantity_entry.get().strip()
            sub_parts = [self.sub_parts_listbox.get(i).split(':')[0] if ':' in self.sub_parts_listbox.get(i) else self.sub_parts_listbox.get(i) for i in self.sub_parts_listbox.curselection()]
            weldment_indicator = self.weldment_var.get() if part_type == "Single Part" else "No"
            top_level_assembly = "N/A" if part_type == "Single Part" else part_id

            input_data = (f"Part Type: {part_type}, Part ID: {part_id}, Revision: {revision}, Material: {material}, "
                          f"Thickness: {thickness}, Lay-Flat: {lay_flat}, Quantity: {quantity}, Sub-Parts: {sub_parts}, "
                          f"Weldment: {weldment_indicator}, Top-Level Assembly: {top_level_assembly}")

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
                if not all([material, thickness, lay_flat]):
                    output = "Material, Thickness, and Lay-Flat are required for single parts"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Single part with empty fields",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return

            thickness = float(thickness) if part_type == "Single Part" else 0.0
            quantity = int(quantity) if part_type == "Assembly" else 1

            if part_type == "Single Part":
                if not re.match(r"^\d+x\d+$", lay_flat):
                    output = "Lay-Flat must be in format 'lengthxwidth' (e.g., 1000x500)"
                    messagebox.showerror("Error", output)
                    log_test_result(
                        test_case="FR2: Invalid lay-flat format",
                        input_data=input_data,
                        output=output,
                        pass_fail="Fail"
                    )
                    return
                length, width = map(int, lay_flat.split('x'))
            else:
                length, width = 0, 0

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
                if material not in ['steel', 'aluminum']:
                    output = "Material must be 'steel' or 'aluminum'"
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
                'catalogue_cost': catalogue_cost
            }

            rates = load_rates()
            if not rates:
                output = "Failed to load rates from rates_global.txt"
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
            output = f"Cost calculated: £{total_cost}\nSaved to output.txt"
            messagebox.showinfo("Success", output)
            log_test_result(
                test_case="FR3-FR4-FR5: Cost calculation and output storage",
                input_data=input_data,
                output=output,
                pass_fail="Pass"
            )
            self.create_quote_screen(part_id, total_cost)
        except ValueError:
            output = "Invalid input: Lay-Flat, quantity must be valid"
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
            3. Calls save_quote to generate and save the quote to quotes.txt.
            4. Logs test result to test_logs.txt using logger.
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
            output = "Quote generated and saved to quotes.txt"
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
        tk.Label(main_frame, text="Rate Key (e.g., steel_rate):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
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
        Update a rate in rates_global.txt (FR6).
        
        Logic:
            1. Retrieves rate key and value from entry fields.
            2. Validates inputs (non-empty key, numeric non-negative value).
            3. Calls update_rates to save the new rate.
            4. Logs test result to test_logs.txt using logger.
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
            output = f"Rate '{rate_key}' updated to {rate_value} in rates_global.txt"
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
