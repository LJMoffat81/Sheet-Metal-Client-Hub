import tkinter as tk
from tkinter import messagebox
import logging
from file_handler import FileHandler
from calculator import calculate_cost

logging.basicConfig(
    filename='gui.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SheetMetalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sheet Metal Client Hub")
        self.file_handler = FileHandler()
        self.rates = self.file_handler.load_rates()
        self.cost = 0.0
        self.part_id = ""
        self.part_data = {}
        self.setup_login_screen()

    def setup_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            logging.warning("Username and password cannot be empty")
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        if self.file_handler.validate_credentials(username, password):
            self.login_frame.destroy()
            if username == "admin":
                self.show_rate_update_screen()
            else:
                self.show_part_input_screen()
        else:
            logging.warning(f"Invalid credentials for user: {username}")
            messagebox.showerror("Error", "Invalid credentials")

    def show_part_input_screen(self):
        self.part_input_frame = tk.Frame(self.root)
        self.part_input_frame.pack(padx=10, pady=10)

        tk.Label(self.part_input_frame, text="Part ID:").grid(row=0, column=0, sticky="e")
        self.part_id_entry = tk.Entry(self.part_input_frame)
        self.part_id_entry.grid(row=0, column=1)

        tk.Label(self.part_input_frame, text="Part Type:").grid(row=1, column=0, sticky="e")
        self.part_type_var = tk.StringVar(value="Part")
        tk.Radiobutton(self.part_input_frame, text="Part", variable=self.part_type_var, value="Part").grid(row=1, column=1, sticky="w")
        tk.Radiobutton(self.part_input_frame, text="Assembly", variable=self.part_type_var, value="Assembly").grid(row=1, column=2, sticky="w")

        tk.Label(self.part_input_frame, text="Material:").grid(row=2, column=0, sticky="e")
        self.material_var = tk.StringVar(value="mild_steel")
        tk.OptionMenu(self.part_input_frame, self.material_var, "mild_steel", "aluminium", "stainless_steel").grid(row=2, column=1)

        tk.Label(self.part_input_frame, text="Thickness (mm):").grid(row=3, column=0, sticky="e")
        self.thickness_entry = tk.Entry(self.part_input_frame)
        self.thickness_entry.grid(row=3, column=1)

        tk.Label(self.part_input_frame, text="Length (mm):").grid(row=4, column=0, sticky="e")
        self.length_entry = tk.Entry(self.part_input_frame)
        self.length_entry.grid(row=4, column=1)

        tk.Label(self.part_input_frame, text="Width (mm):").grid(row=5, column=0, sticky="e")
        self.width_entry = tk.Entry(self.part_input_frame)
        self.width_entry.grid(row=5, column=1)

        tk.Label(self.part_input_frame, text="Quantity:").grid(row=6, column=0, sticky="e")
        self.quantity_entry = tk.Entry(self.part_input_frame)
        self.quantity_entry.grid(row=6, column=1)

        tk.Label(self.part_input_frame, text="Work Centres:").grid(row=7, column=0, sticky="e")
        self.work_centre_var = tk.StringVar()
        work_centres = ['cutting', 'bending', 'welding']
        self.work_centre_menu = tk.OptionMenu(self.part_input_frame, self.work_centre_var, *work_centres)
        self.work_centre_menu.grid(row=7, column=1)

        tk.Button(self.part_input_frame, text="Submit", command=self.submit_part).grid(row=8, column=0, columnspan=2, pady=5)

    def submit_part(self):
        try:
            self.part_id = self.part_id_entry.get()
            part_type = self.part_type_var.get()
            quantity = int(self.quantity_entry.get())
            self.part_data = {
                'part_type': part_type,
                'quantity': quantity,
                'work_centres': [self.work_centre_var.get()] if self.work_centre_var.get() else []
            }

            if part_type == "Part":
                material = self.material_var.get()
                thickness = float(self.thickness_entry.get())
                length = float(self.length_entry.get())
                width = float(self.width_entry.get())

                if thickness <= 0 or length <= 0 or width <= 0:
                    logging.error("Invalid dimensions")
                    messagebox.showerror("Error", "Dimensions must be positive")
                    return

                self.part_data.update({
                    'material': material,
                    'thickness': thickness,
                    'length': length,
                    'width': width
                })
            else:
                self.part_data.update({
                    'material': 'N/A',
                    'thickness': 0.0,
                    'length': 0.0,
                    'width': 0.0,
                    'components': quantity
                })

            self.cost = calculate_cost(self.part_data, self.rates)
            if self.cost == 0.0:
                messagebox.showerror("Error", "Cost calculation failed")
                return

            self.file_handler.save_output(f"{self.part_id},{quantity},{self.part_data['material']},{self.part_data['thickness']},{self.part_data['length']},{self.part_data['width']},1,{self.cost}")
            self.part_input_frame.destroy()
            self.show_quote_screen()
        except ValueError as e:
            logging.error(f"Invalid input: {str(e)}")
            messagebox.showerror("Error", "Invalid input values")

    def show_quote_screen(self):
        self.quote_frame = tk.Frame(self.root)
        self.quote_frame.pack(padx=10, pady=10)

        tk.Label(self.quote_frame, text=f"Cost: ${self.cost:.2f}").grid(row=0, column=0, columnspan=2)
        tk.Label(self.quote_frame, text="Customer Name:").grid(row=1, column=0, sticky="e")
        self.customer_entry = tk.Entry(self.quote_frame)
        self.customer_entry.grid(row=1, column=1)

        tk.Label(self.quote_frame, text="Profit Margin (%):").grid(row=2, column=0, sticky="e")
        self.margin_entry = tk.Entry(self.quote_frame)
        self.margin_entry.grid(row=2, column=1)

        tk.Button(self.quote_frame, text="Generate Quote", command=self.generate_quote).grid(row=3, column=0, columnspan=2, pady=5)

    def generate_quote(self):
        try:
            customer = self.customer_entry.get()
            margin = float(self.margin_entry.get())
            if not customer or margin < 0:
                logging.error("Invalid customer or margin")
                messagebox.showerror("Error", "Invalid customer name or margin")
                return
            quote_data = {
                'part_id': self.part_id,
                'total_cost': self.cost * (1 + margin / 100),
                'customer_name': customer,
                'profit_margin': margin
            }
            self.file_handler.save_quote(json.dumps(quote_data))
            messagebox.showinfo("Success", "Quote generated successfully")
            self.quote_frame.destroy()
            self.setup_login_screen()
        except ValueError as e:
            logging.error(f"Invalid margin: {str(e)}")
            messagebox.showerror("Error", "Invalid margin value")

    def show_rate_update_screen(self):
        self.rate_frame = tk.Frame(self.root)
        self.rate_frame.pack(padx=10, pady=10)

        tk.Label(self.rate_frame, text="Rate Key:").grid(row=0, column=0, sticky="e")
        self.rate_key_var = tk.StringVar()
        rate_keys = ['mild_steel_rate', 'aluminium_rate', 'cutting_rate_per_mm', 'bending_rate_per_bend']
        tk.OptionMenu(self.rate_frame, self.rate_key_var, *rate_keys).grid(row=0, column=1)

        tk.Label(self.rate_frame, text="Rate Value:").grid(row=1, column=0, sticky="e")
        self.rate_value_entry = tk.Entry(self.rate_frame)
        self.rate_value_entry.grid(row=1, column=1)

        tk.Button(self.rate_frame, text="Update Rate", command=self.update_rate).grid(row=2, column=0, columnspan=2, pady=5)

    def update_rate(self):
        try:
            key = self.rate_key_var.get()
            value = float(self.rate_value_entry.get())
            if value < 0:
                logging.error("Invalid rate value")
                messagebox.showerror("Error", "Rate value must be non-negative")
                return
            self.file_handler.update_rates(key, value)
            self.rates = self.file_handler.load_rates()
            messagebox.showinfo("Success", f"Rate {key} updated to {value}")
            self.rate_frame.destroy()
            self.setup_login_screen()
        except ValueError as e:
            logging.error(f"Invalid rate value: {str(e)}")
            messagebox.showerror("Error", "Invalid rate value")

if __name__ == "__main__":
    root = tk.Tk()
    app = SheetMetalGUI(root)
    root.mainloop()
