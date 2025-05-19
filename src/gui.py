# gui.py
# Purpose: Implements the graphical user interface (GUI) using Tkinter for the Sheet Metal Client Hub.
# Supports FR1 (Login), FR2 (Part Input), FR6 (Update Rates), FR7 (Generate Quote).
# Provides screens for login, part input, quote generation, and admin rate updates.
# Integrates with calculator.py for cost calculations and file_handler.py for file operations.
# Uses messagebox for user feedback (success/error messages).
# Designed for Python 3.9 with Tkinter, supporting 10 work centres, GBP, and mm units.

import tkinter as tk
from tkinter import messagebox
from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates
from calculator import calculate_cost

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
            2. Sets the window title.
            3. Initializes role as None (set after login).
            4. Displays the login screen.
        """
        self.root = root
        self.root.title("Sheet Metal Client Hub")
        self.role = None
        self.create_login_screen()

    def create_login_screen(self):
        """
        Create the login screen for user authentication (FR1).
        
        Logic:
            1. Clears existing widgets.
            2. Adds username and password entry fields.
            3. Adds a login button that calls the login method.
        """
        self.clear_screen()
        tk.Label(self.root, text="Username:").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        tk.Button(self.root, text="Login", command=self.login).pack()

    def login(self):
        """
        Handle login button click and validate credentials (FR1).
        
        Logic:
            1. Gets username and password from entry fields.
            2. Calls validate_credentials to check against users.txt.
            3. If valid, sets role ("Admin" for username "admin", else "User").
            4. Shows success message and navigates to part input (User) or admin screen.
            5. If invalid, shows error message and keeps login screen.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        if validate_credentials(username, password):
            self.role = "Admin" if username == "admin" else "User"
            messagebox.showinfo("Success", "Login successful")
            if self.role == "User":
                self.create_part_input_screen()
            else:
                self.create_admin_screen()
        else:
            messagebox.showerror("Error", "Invalid credentials, please try again")

    def create_part_input_screen(self):
        """
        Create the part input screen for entering part specifications (FR2).
        
        Logic:
            1. Clears existing widgets.
            2. Adds entry fields for part ID, revision, material, thickness, length, width, quantity.
            3. Adds a button to calculate cost, calling calculate_and_save.
        """
        self.clear_screen()
        tk.Label(self.root, text="Part ID:").pack()
        self.part_id_entry = tk.Entry(self.root)
        self.part_id_entry.pack()
        tk.Label(self.root, text="Revision:").pack()
        self.revision_entry = tk.Entry(self.root)
        self.revision_entry.pack()
        tk.Label(self.root, text="Material (steel/aluminum):").pack()
        self.material_entry = tk.Entry(self.root)
        self.material_entry.pack()
        tk.Label(self.root, text="Thickness (mm):").pack()
        self.thickness_entry = tk.Entry(self.root)
        self.thickness_entry.pack()
        tk.Label(self.root, text="Length (mm):").pack()
        self.length_entry = tk.Entry(self.root)
        self.length_entry.pack()
        tk.Label(self.root, text="Width (mm):").pack()
        self.width_entry = tk.Entry(self.root)
        self.width_entry.pack()
        tk.Label(self.root, text="Quantity:").pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()
        tk.Button(self.root, text="Calculate Cost", command=self.calculate_and_save).pack()

    def calculate_and_save(self):
        """
        Calculate cost and save output based on part specifications (FR2, FR3, FR4, FR5).
        
        Logic:
            1. Retrieves part specifications from entry fields.
            2. Validates inputs (numeric values, thickness 1-3 mm).
            3. Loads rates from rates_global.txt.
            4. Calls calculate_cost to compute total cost.
            5. Saves result to output.txt using save_output.
            6. Shows success message with cost.
            7. Navigates to quote screen.
            8. Handles errors (e.g., invalid inputs) with error messages.
        """
        try:
            part_id = self.part_id_entry.get()
            revision = self.revision_entry.get()
            material = self.material_entry.get().lower()
            thickness = float(self.thickness_entry.get())
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            quantity = int(self.quantity_entry.get())

            if thickness < 1 or thickness > 3 or length <= 0 or width <= 0 or quantity <= 0:
                messagebox.showerror("Error", "Invalid part specifications: thickness must be 1-3 mm, others positive")
                return

            rates = load_rates()
            total_cost = calculate_cost(part_id, revision, material, thickness, length, width, quantity, rates)
            save_output(part_id, revision, material, thickness, length, width, quantity, total_cost)
            messagebox.showinfo("Success", f"Cost calculated: £{total_cost}\nSaved to output.txt")
            self.create_quote_screen(part_id, total_cost)
        except ValueError:
            messagebox.showerror("Error", "Invalid input: please enter numeric values for thickness, length, width, quantity")

    def create_quote_screen(self, part_id, total_cost):
        """
        Create the quote generation screen (FR7).
        
        Parameters:
            part_id (str): Part identifier.
            total_cost (float): Calculated cost from calculate_cost.
        
        Logic:
            1. Clears existing widgets.
            2. Adds entry fields for customer name and profit margin.
            3. Adds a button to generate the quote, calling generate_quote.
        """
        self.clear_screen()
        tk.Label(self.root, text="Customer Name:").pack()
        self.customer_entry = tk.Entry(self.root)
        self.customer_entry.pack()
        tk.Label(self.root, text="Profit Margin (%):").pack()
        self.margin_entry = tk.Entry(self.root)
        self.margin_entry.pack()
        tk.Button(self.root, text="Generate Quote", command=lambda: self.generate_quote(part_id, total_cost)).pack()

    def generate_quote(self, part_id, total_cost):
        """
        Generate and save a quote (FR7).
        
        Parameters:
            part_id (str): Part identifier.
            total_cost (float): Calculated cost.
        
        Logic:
            1. Retrieves customer name and profit margin from entry fields.
            2. Validates profit margin as numeric.
            3. Calls save_quote to generate and save the quote to quotes.txt.
            4. Shows success message.
            5. Returns to part input screen.
            6. Handles errors with error messages.
        """
        try:
            customer_name = self.customer_entry.get()
            profit_margin = float(self.margin_entry.get())
            save_quote(part_id, total_cost, customer_name, profit_margin)
            messagebox.showinfo("Success", "Quote generated and saved to quotes.txt")
            self.create_part_input_screen()
        except ValueError:
            messagebox.showerror("Error", "Invalid profit margin: please enter a numeric value")

    def create_admin_screen(self):
        """
        Create the admin screen for updating rates (FR6).
        
        Logic:
            1. Clears existing widgets.
            2. Adds entry fields for rate key (e.g., steel_rate) and value (GBP).
            3. Adds a button to update the rate, calling update_rate.
            4. Adds a button to access user features (part input).
        """
        self.clear_screen()
        tk.Label(self.root, text="Rate Key (e.g., steel_rate):").pack()
        self.rate_key_entry = tk.Entry(self.root)
        self.rate_key_entry.pack()
        tk.Label(self.root, text="Rate Value (GBP):").pack()
        self.rate_value_entry = tk.Entry(self.root)
        self.rate_value_entry.pack()
        tk.Button(self.root, text="Update Rate", command=self.update_rate).pack()
        tk.Button(self.root, text="User Features", command=self.create_part_input_screen).pack()

    def update_rate(self):
        """
        Update a rate in rates_global.txt (FR6).
        
        Logic:
            1. Retrieves rate key and value from entry fields.
            2. Validates value as numeric.
            3. Calls update_rates to save the new rate.
            4. Shows success message.
            5. Handles errors with error messages.
        """
        try:
            rate_key = self.rate_key_entry.get()
            rate_value = float(self.rate_value_entry.get())
            update_rates(rate_key, rate_value)
            messagebox.showinfo("Success", "Rates updated in rates_global.txt")
        except ValueError:
            messagebox.showerror("Error", "Invalid rate value: please enter a numeric value")

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
    root = tk.Tk()
    app = SheetMetalClientHub(root)
    root.mainloop()
