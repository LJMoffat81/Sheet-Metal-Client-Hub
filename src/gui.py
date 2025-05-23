# gui.py
# Purpose: Implements the graphical user interface (GUI) using Tkinter for the Sheet Metal Client Hub.
# Supports FR1 (Login), FR2 (Part Input), FR6 (Update Rates), FR7 (Generate Quote).
# Provides screens for login, part input, quote generation, and admin rate updates with a consistent footer.
# Integrates with calculator.py for cost calculations and file_handler.py for file operations.
# Uses messagebox for user feedback and logger.py for automatic test result logging.
# Designed for Python 3.9 with Tkinter, supporting 10 work centres, GBP, and mm units.

import tkinter as tk
from tkinter import messagebox, Toplevel
import os
import re
from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates
from calculator import calculate_cost
from logger import log_test_result

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
            - Assembly: Show Part ID, Revision, Quantity, Sub-Parts dropdown.
            - Single Part: Show Part ID, Revision, Material, Thickness, Lay-Flat Length/Width, Weldment, Fasteners/Inserts dropdown.
            - WorkCentre operations always visible on right side.
        """
        part_type = self.part_type_var.get()
        
        # Hide all part input fields initially
        for widget in [self.part_id_label, self.part_id_entry,
                       self.revision_label, self.revision_entry,
                       self.material_label, self.material_option,
                       self.thickness_label, self.thickness_option,
                       self.lay_flat_length_label, self.lay_flat_length_option,
                       self.lay_flat_width_label, self.lay_flat_width_option,
                       self.quantity_label, self.quantity_option, self.custom_quantity_entry,
                       self.sub_parts_label, self.sub_parts_option, self.add_sub_part_button,
                       self.clear_sub_parts_button, self.selected_sub_parts_label,
                       self.weldment_label, self.weldment_option,
                       self.settings_button, self.back_button, self.add_another_part_button]:
            widget.grid_remove()
        
        # Show common fields (right-aligned)
        self.part_id_label.grid(row=2, column=0, padx=(10, 2), pady=2, sticky="e")
        self.part_id_entry.grid(row=2, column=1, padx=(2, 5), pady=2, sticky="w")
        self.revision_label.grid(row=3, column=0, padx=(10, 2), pady=2, sticky="e")
        self.revision_entry.grid(row=3, column=1, padx=(2, 5), pady=2, sticky="w")
        
        if part_type == "Assembly":
            self.quantity_label.grid(row=4, column=0, padx=(10, 2), pady=2, sticky="e")
            self.quantity_option.grid(row=4, column=1, padx=(2, 5), pady=2, sticky="w")
            self.custom_quantity_entry.grid(row=5, column=1, padx=(2, 5), pady=2, sticky="w")
            self.sub_parts_label.grid(row=6, column=0, padx=(10, 2), pady=2, sticky="e")
            self.sub_parts_option.grid(row=6, column=1, padx=(2, 5), pady=2, sticky="w")
            self.add_sub_part_button.grid(row=7, column=1, padx=(2, 5), pady=2, sticky="w")
            self.clear_sub_parts_button.grid(row=8, column=1, padx=(2, 5), pady=2, sticky="w")
            self.selected_sub_parts_label.grid(row=9, column=0, columnspan=2, padx=(10, 5), pady=2, sticky="w")
            self.settings_button.grid(row=10, column=1, padx=(2, 5), pady=2, sticky="w")
            self.back_button.grid(row=11, column=1, padx=(2, 5), pady=2, sticky="w")
            self.add_another_part_button.grid(row=12, column=1, padx=(2, 5), pady=2, sticky="w")
        else:  # Single Part
            self.material_label.grid(row=4, column=0, padx=(10, 2), pady=2, sticky="e")
            self.material_option.grid(row=4, column=1, padx=(2, 5), pady=2, sticky="w")
            self.thickness_label.grid(row=5, column=0, padx=(10, 2), pady=2, sticky="e")
            self.thickness_option.grid(row=5, column=1, padx=(2, 5), pady=2, sticky="w")
            self.lay_flat_length_label.grid(row=6, column=0, padx=(10, 2), pady=2, sticky="e")
            self.lay_flat_length_option.grid(row=6, column=1, padx=(2, 5), pady=2, sticky="w")
            self.lay_flat_width_label.grid(row=7, column=0, padx=(10, 2), pady=2, sticky="e")
            self.lay_flat_width_option.grid(row=7, column=1, padx=(2, 5), pady=2, sticky="w")
            self.weldment_label.grid(row=8, column=0, padx=(10, 2), pady=2, sticky="e")
            self.weldment_option.grid(row=8, column=1, padx=(2, 5), pady=2, sticky="w")
            self.sub_parts_label.grid(row=9, column=0, padx=(10, 2), pady=2, sticky="e")
            self.sub_parts_option.grid(row=9, column=1, padx=(2, 5), pady=2, sticky="w")
            self.add_sub_part_button.grid(row=10, column=1, padx=(2, 5), pady=2, sticky="w")
            self.clear_sub_parts_button.grid(row=11, column=1, padx=(2, 5), pady=2, sticky="w")
            self.selected_sub_parts_label.grid(row=12, column=0, columnspan=2, padx=(10, 5), pady=2, sticky="w")
            self.settings_button.grid(row=13, column=1, padx=(2, 5), pady=2, sticky="w")
            self.back_button.grid(row=14, column=1, padx=(2, 5), pady=2, sticky="w")
            self.add_another_part_button.grid(row=15, column=1, padx=(2, 5), pady=2, sticky="w")

        # Update sub-parts dropdown content
        self.update_sub_parts_dropdown()

    def update_sub_parts_dropdown(self):
        """
        Update the sub-parts dropdown based on part type.
        - Assembly: Load existing parts from data/output.txt.
        - Single Part: Load fasteners/inserts from data/parts_catalogue.txt.
        """
        self.sub_parts_var.set("Select Item")
        menu = self.sub_parts_option['menu']
        menu.delete(0, tk.END)
        menu.add_command(label="Select Item", command=lambda: self.sub_parts_var.set("Select Item"))
        
        if self.part_type_var.get() == "Assembly":
            existing_parts = load_existing_parts()
            if existing_parts:
                for part_id in existing_parts:
                    menu.add_command(label=part_id, command=lambda x=part_id: self.sub_parts_var.set(x))
            else:
                menu.add_command(label="No parts available", command=lambda: self.sub_parts_var.set("No parts available"))
        else:  # Single Part
            catalogue = load_parts_catalogue()
            if catalogue:
                for item_id, description, _ in catalogue:
                    label = f"{item_id}: {description}"
                    menu.add_command(label=label, command=lambda x=label: self.sub_parts_var.set(x))
            else:
                menu.add_command(label="No catalogue items available", command=lambda: self.sub_parts_var.set("No catalogue items available"))

    def add_sub_part(self):
        """
        Add the selected sub-part or fastener to the list of selected items.
        Update the display in selected_sub_parts_label.
        """
        selected_item = self.sub_parts_var.get()
        if selected_item and selected_item not in ["Select Item", "No parts available", "No catalogue items available"]:
            if selected_item not in self.selected_sub_parts:
                self.selected_sub_parts.append(selected_item)
                self.selected_sub_parts_label.config(text=f"Selected Items: {', '.join(self.selected_sub_parts)}")
            self.sub_parts_var.set("Select Item")

    def clear_sub_parts(self):
        """
        Clear all selected sub-parts or fasteners and update the display.
        """
        self.selected_sub_parts = []
        self.selected_sub_parts_label.config(text="Selected Items: None")

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
        self.part_type_var.set("Single Part")
        self.material_var.set("Mild Steel")
        self.thickness_var.set("1.0")
        self.lay_flat_length_var.set("1000")
        self.lay_flat_width_var.set("500")
        self.quantity_var.set("1")
        self.custom_quantity_entry.delete(0, tk.END)
        self.custom_quantity_entry.config(state='disabled')
        self.weldment_var.set("No")
        self.selected_sub_parts = []
        self.selected_sub_parts_label.config(text="Selected Items: None")
        self.sub_parts_var.set("Select Item")
        for var in self.work_centre_vars:
            var.set("None")
        self.add_another_part_button.config(state='disabled')
        self.submit_button.config(state='disabled')
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
            2. Creates main content frame with a vertical split (left: part inputs, right: Planned Manufacture Operations).
            3. Left side: Conditional fields, right-aligned near centerline, with navigation buttons.
            4. Right side: Planned Manufacture Operations with 10 operations, centered title/buttons.
            5. Adds a centered vertical line and footer.
        """
        self.clear_screen()
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left side: Part input data
        left_frame = tk.Frame(main_frame, width=500)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)
        tk.Label(left_frame, text="Part Input", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Part Type
        self.part_type_label = tk.Label(left_frame, text="Part Type:", font=("Arial", 12))
        self.part_type_label.grid(row=1, column=0, padx=(10, 2), pady=2, sticky="e")
        self.part_type_var = tk.StringVar(value="Single Part")
        self.part_type_var.trace("w", self.update_part_input_fields)
        self.part_type_option = tk.OptionMenu(left_frame, self.part_type_var, "Single Part", "Assembly")
        self.part_type_option.grid(row=1, column=1, padx=(2, 5), pady=2, sticky="w")

        # Initialize all part input fields
        self.part_id_label = tk.Label(left_frame, text="Part ID:", font=("Arial", 12))
        self.part_id_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.revision_label = tk.Label(left_frame, text="Revision:", font=("Arial", 12))
        self.revision_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.material_label = tk.Label(left_frame, text="Material:", font=("Arial", 12))
        self.material_var = tk.StringVar(value="Mild Steel")
        self.material_option = tk.OptionMenu(left_frame, self.material_var, "Mild Steel", "Aluminium", "Stainless Steel")
        self.thickness_label = tk.Label(left_frame, text="Thickness (mm):", font=("Arial", 12))
        self.thickness_var = tk.StringVar(value="1.0")
        self.thickness_option = tk.OptionMenu(left_frame, self.thickness_var, "1.0", "1.2", "1.5", "2.0", "2.5", "3.0")
        self.lay_flat_length_label = tk.Label(left_frame, text="Lay-Flat Length (mm):", font=("Arial", 12))
        self.lay_flat_length_var = tk.StringVar(value="1000")
        self.lay_flat_length_option = tk.OptionMenu(left_frame, self.lay_flat_length_var, "50", "100", "500", "1000", "1500", "2000", "3000")
        self.lay_flat_width_label = tk.Label(left_frame, text="Lay-Flat Width (mm):", font=("Arial", 12))
        self.lay_flat_width_var = tk.StringVar(value="500")
        self.lay_flat_width_option = tk.OptionMenu(left_frame, self.lay_flat_width_var, "50", "100", "500", "1000", "1500")
        self.quantity_label = tk.Label(left_frame, text="Quantity:", font=("Arial", 12))
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_var.trace("w", lambda *args: self.update_quantity_entry_state())
        self.quantity_option = tk.OptionMenu(left_frame, self.quantity_var, "1", "5", "10", "20", "50", "100", "Other")
        self.custom_quantity_entry = tk.Entry(left_frame, font=("Arial", 12), state='disabled')
        self.sub_parts_label = tk.Label(left_frame, text="Sub-Parts/Fasteners:", font=("Arial", 12))
        self.sub_parts_var = tk.StringVar(value="Select Item")
        self.sub_parts_option = tk.OptionMenu(left_frame, self.sub_parts_var, "Select Item")
        self.add_sub_part_button = tk.Button(left_frame, text="Add Sub-Part/Fastener", command=self.add_sub_part, font=("Arial", 12))
        self.clear_sub_parts_button = tk.Button(left_frame, text="Clear Selected Sub-Parts", command=self.clear_sub_parts, font=("Arial", 12))
        self.selected_sub_parts_label = tk.Label(left_frame, text="Selected Items: None", font=("Arial", 12), wraplength=400, justify="left")
        self.weldment_label = tk.Label(left_frame, text="Weldment Indicator:", font=("Arial", 12))
        self.weldment_var = tk.StringVar(value="No")
        self.weldment_option = tk.OptionMenu(left_frame, self.weldment_var, "Yes", "No")
        self.settings_button = tk.Button(left_frame, text="Settings", command=self.go_to_settings, font=("Arial", 12))
        self.back_button = tk.Button(left_frame, text="Back", command=self.go_back_to_login, font=("Arial", 12))
        self.add_another_part_button = tk.Button(left_frame, text="Add Another Part", command=self.reset_part_input, font=("Arial", 12), state='disabled')

        # Initialize selected sub-parts list
        self.selected_sub_parts = []

        # Populate sub-parts dropdown and show initial fields
        self.update_part_input_fields()
        self.part_type_var.set("Single Part")  # Trigger initial update

        # Central vertical line (exactly at 500px)
        separator = tk.Canvas(main_frame, width=2, bg="black")
        separator.pack(side=tk.LEFT, fill=tk.Y)

        # Right side: Planned Manufacture Operations (always visible, centered)
        right_frame = tk.Frame(main_frame, width=500)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=2, pady=2)
        tk.Label(right_frame, text="Planned Manufacture Operations", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5))

        # WorkCentre options
        work_centres = [
            "Cutting", "Bending", "Welding", "Assembly", "Finishing",
            "Drilling", "Punching", "Grinding", "Coating", "Inspection"
        ]
        self.work_centre_vars = []
        for i in range(10):  # Operations 10 to 100
            op_label = f"Operation {(i+1)*10}:"
            tk.Label(right_frame, text=op_label, font=("Arial", 10)).grid(row=i+1, column=0, padx=(50, 2), pady=2, sticky="e")
            var = tk.StringVar(value="None")
            tk.OptionMenu(right_frame, var, "None", *work_centres).grid(row=i+1, column=1, padx=(2, 50), pady=2, sticky="w")
            self.work_centre_vars.append(var)

        # Calculate Cost and Submit buttons
        self.calculate_cost_button = tk.Button(right_frame, text="Calculate Cost", command=self.calculate_and_save, font=("Arial", 10))
        self.calculate_cost_button.grid(row=11, column=0, columnspan=2, pady=5)
        self.submit_button = tk.Button(right_frame, text="Submit", command=lambda: self.create_quote_screen(self.last_part_id, self.last_total_cost), font=("Arial", 10), state='disabled')
        self.submit_button.grid(row=12, column=0, columnspan=2, pady=5)

        # Footer
        footer = tk.Frame(self.root)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.create_footer(footer)

    def calculate_and_save(self):
        """
        Calculate cost and save output based on part specifications (FR2, FR3, FR4, FR5).
        
        Logic:
            1. Retrieves part specifications based on part type.
            2. Validates inputs, including WorkCentre operations.
            3. Calculates cost including catalogue items and WorkCentres.
            4. Saves result and enables Add Another Part/Submit buttons.
            5. Stores part_id and total_cost for Submit button.
        """
        try:
            part_type = self.part_type_var.get()
            part_id = self.part_id_entry.get().strip()
            revision = self.revision_entry.get().strip()
            material = self.material_var.get().lower() if part_type == "Single Part" else "N/A"
            thickness = self.thickness_var.get() if part_type == "Single Part" else "0.0"
            length = self.lay_flat_length_var.get() if part_type == "Single Part" else "0"
            width = self.lay_flat_width_var.get() if part_type == "Single Part" else "0"
            quantity = self.quantity_var.get() if part_type == "Assembly" else "1"
            if quantity == "Other":
                quantity = self.custom_quantity_entry.get().strip()
            sub_parts = self.selected_sub_parts
            weldment_indicator = self.weldment_var.get() if part_type == "Single Part" else "No"
            top_level_assembly = "N/A" if part_type == "Single Part" else part_id
            work_centres = [var.get() for var in self.work_centre_vars if var.get() != "None"]

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
                    item_id = item_id.split(':')[0].strip()  # Extract item_id from "item_id: description"
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
            # Enable Add Another Part and Submit buttons
            self.add_another_part_button.config(state='normal')
            self.submit_button.config(state='normal')
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
