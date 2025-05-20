gui.py
Purpose: Implements the graphical user interface (GUI) using Tkinter for the Sheet Metal Client Hub.
Supports FR1 (Login), FR2 (Part Input), FR6 (Update Rates), FR7 (Generate Quote).
Provides screens for login, part input, quote generation, and admin rate updates with a consistent footer.
Integrates with calculator.py for cost calculations and file_handler.py for file operations.
Uses messagebox for user feedback and logger.py for automatic test result logging.
Designed for Python 3.9 with Tkinter, supporting 10 work centres, GBP, and mm units.
import tkinter as tk
from tkinter import messagebox
import os
import re
from file_handler import validate_credentials, load_rates, save_output, save_quote, update_rates
from calculator import calculate_cost
from logger import log_test_result

Get the absolute path to the repository root for icon
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(file)))

class SheetMetalClientHub:
"""
Main GUI class for the Sheet Metal Client Hub application.
Manages all screens (login, part input, quote, admin) and user interactions.
"""
def init(self, root):
"""
Initialize the GUI application.

Parameters:
root (tk.Tk): The Tkinter root window.

Logic:

Stores the root window.
Sets the window title and fixed size to 1000x750 pixels.
Sets a custom laser icon.
Initializes role as None (set after login).
Displays the login screen. """ self.root = root self.root.title("Sheet Metal Client Hub") self.root.geometry("1000x750") self.root.resizable(False, False) # Prevent resizing self.root.minsize(400, 400) # Set minimum size as fallback
Set custom laser icon
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

Adds version label on the left.
Adds help button on the right that opens a guide. """ frame.configure(bg="lightgrey") tk.Label(frame, text="Version 1.0", font=("Arial", 10), bg="lightgrey").pack(side=tk.LEFT, padx=10, pady=5) tk.Button(frame, text="Help", command=self.show_help, font=("Arial", 10), bg="lightgrey").pack(side=tk.RIGHT, padx=10, pady=5)
def show_help(self):
"""
Display a help guide for the application.

Logic:

Shows a messagebox with a placeholder guide.
Logs the help action to test_logs.txt. """ guide = ( "Sheet Metal Client Hub - User Guide\n\n" "1. Login: Enter username and password (e.g., laurie:moffat123).\n" "2. Part Input: Select part details (material, thickness, etc.) and calculate cost.\n" "3. Quote: Generate a quote with customer name and profit margin.\n" "4. Admin: Update rates (e.g., steel_rate) if admin.\n" "For support, contact [support email]." ) messagebox.showinfo("Help - Sheet Metal Client Hub", guide) log_test_result( test_case="Help Guide Accessed", input_data="None", output="Help guide displayed", pass_fail="Pass" )
def create_login_screen(self):
"""
Create the login screen for user authentication (FR1).

Logic:

Clears existing widgets.
Creates main content frame and footer.
Adds title, username/password fields, login/clear buttons in main frame.
Sets focus on username field and binds Enter key to login. """ self.clear_screen()
Main content
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
self.root.bind('<return>', lambda event: self.login())</return>

Footer
footer = tk.Frame(self.root)
footer.pack(side=tk.BOTTOM, fill=tk.X)
self.create_footer(footer)

def clear_login_fields(self):
"""
Clear username and password entry fields.

Logic:

Deletes all text in username and password entries.
Sets focus back to username field. """ self.username_entry.delete(0, tk.END) self.password_entry.delete(0, tk.END) self.username_entry.focus_set() log_test_result( test_case="FR1: Clear login fields", input_data="None", output="Username and password fields cleared", pass_fail="Pass" )
def login(self):
"""
Handle login button click and validate credentials (FR1).

Logic:

Gets username and password from entry fields.
Validates inputs (non-empty).
Calls validate_credentials to check against users.txt.
Sets role ("Admin" for username "admin", else "User").
Logs test result to test_logs.txt using logger.
Shows success message and navigates to appropriate screen.
Shows and logs error message for invalid inputs or credentials. """ username = self.username_entry.get().strip() password = self.password_entry.get().strip() if not username or not password: output = "Username and password cannot be empty" messagebox.showerror("Error", output) log_test_result( test_case="FR1: Login with empty fields", input_data=f"Username: {username}, Password: {password}", output=output, pass_fail="Fail" ) return if validate_credentials(username, password): self.role = "Admin" if username == "admin" else "User" output = f"Login successful as {self.role}" messagebox.showinfo("Success", output) log_test_result( test_case=f"FR1: Valid {self.role} login", input_data=f"Username: {username}, Password: [hidden]", output=output, pass_fail="Pass" ) if self.role == "User": self.create_part_input_screen() else: self.create_admin_screen() else: output = "Invalid username or password" messagebox.showerror("Error", output) log_test_result( test_case="FR1: Invalid login", input_data=f"Username: {username}, Password: [hidden]", output=output, pass_fail="Fail" )
def update_quantity_entry_state(self):
"""
Enable or disable the custom quantity entry based on the quantity dropdown selection.
Logic:

If "Other" is selected, enable the custom quantity entry.
Otherwise, disable it. """ if self.quantity_var.get() == "Other": self.custom_quantity_entry.config(state='normal') else: self.custom_quantity_entry.config(state='disabled')
def create_part_input_screen(self):
"""
Create the part input screen for entering part specifications (FR2).

Logic:

Clears existing widgets.
Creates main content frame and footer.
Adds fields for part type, ID, revision, material, thickness, length, width, quantity, cutting inputs.
Adds assembly-specific fields (sub-parts listbox, top-level assembly, weldment indicator).
Adds button to calculate cost. """ self.clear_screen()
Main content
main_frame = tk.Frame(self.root)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
tk.Label(main_frame, text="Part Input", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

Part Type
tk.Label(main_frame, text="Part Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
self.part_type_var = tk.StringVar(value="Single Part")
tk.OptionMenu(main_frame, self.part_type_var, "Single Part", "Assembly").grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="w")

Standard fields
tk.Label(main_frame, text="Part ID:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
self.part_id_entry = tk.Entry(main_frame, font=("Arial", 12))
self.part_id_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
tk.Label(main_frame, text="Revision:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
self.revision_entry = tk.Entry(main_frame, font=("Arial", 12))
self.revision_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=5)
tk.Label(main_frame, text="Material:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="e")
self.material_var = tk.StringVar(value="steel")
tk.OptionMenu(main_frame, self.material_var, "steel", "aluminum").grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Thickness (mm):", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="e")
self.thickness_var = tk.StringVar(value="1.0")
tk.OptionMenu(main_frame, self.thickness_var, "1.0", "1.2", "1.5", "2.0", "2.5", "3.0").grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Length (mm):", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="e")
self.length_entry = tk.Entry(main_frame, font=("Arial", 12))
self.length_entry.grid(row=6, column=1, columnspan=2, padx=10, pady=5)
tk.Label(main_frame, text="Width (mm):", font=("Arial", 12)).grid(row=7, column=0, padx=10, pady=5, sticky="e")
self.width_entry = tk.Entry(main_frame, font=("Arial", 12))
self.width_entry.grid(row=7, column=1, columnspan=2, padx=10, pady=5)
tk.Label(main_frame, text="Quantity:", font=("Arial", 12)).grid(row=8, column=0, padx=10, pady=5, sticky="e")
self.quantity_var = tk.StringVar(value="1")
self.quantity_var.trace("w", lambda *args: self.update_quantity_entry_state())
tk.OptionMenu(main_frame, self.quantity_var, "1", "5", "10", "20", "50", "100", "Other").grid(row=8, column=1, padx=10, pady=5, sticky="w")
self.custom_quantity_entry = tk.Entry(main_frame, font=("Arial", 12), state='disabled')
self.custom_quantity_entry.grid(row=8, column=2, padx=10, pady=5, sticky="w")

Assembly-specific fields
self.sub_parts_frame = tk.Frame(main_frame)
tk.Label(self.sub_parts_frame, text="Sub-Parts:", font=("Arial", 12)).pack()
self.sub_parts_listbox = tk.Listbox(self.sub_parts_frame, height=5, width=30)
self.sub_parts_listbox.pack()
tk.Button(self.sub_parts_frame, text="Add Sub-Part", command=self.add_sub_part, font=("Arial", 12)).pack()
tk.Button(self.sub_parts_frame, text="Remove Sub-Part", command=self.remove_sub_part, font=("Arial", 12)).pack()
self.sub_parts_frame.grid(row=9, column=0, columnspan=3, pady=5)

tk.Label(main_frame, text="Top-Level Assembly:", font=("Arial", 12)).grid(row=10, column=0, padx=10, pady=5, sticky="e")
self.top_level_assembly_entry = tk.Entry(main_frame, font=("Arial", 12))
self.top_level_assembly_entry.grid(row=10, column=1, columnspan=2, padx=10, pady=5)
tk.Label(main_frame, text="Weldment Indicator:", font=("Arial", 12)).grid(row=11, column=0, padx=10, pady=5, sticky="e")
self.weldment_var = tk.StringVar(value="No")
tk.OptionMenu(main_frame, self.weldment_var, "Yes", "No").grid(row=11, column=1, columnspan=2, padx=10, pady=5, sticky="w")

Cutting inputs (FR2.1)
tk.Label(main_frame, text="Cutting Method:", font=("Arial", 12)).grid(row=12, column=0, padx=10, pady=5, sticky="e")
self.cutting_method_var = tk.StringVar(value="None")
tk.OptionMenu(main_frame, self.cutting_method_var, "Laser Cutting", "Turret Press Punching", "None").grid(row=12, column=1, columnspan=2, padx=10, pady=5, sticky="w")
tk.Label(main_frame, text="Cutting Complexity:", font=("Arial", 12)).grid(row=13, column=0, padx=10, pady=5, sticky="e")
self.cutting_complexity_var = tk.StringVar(value="1")
tk.OptionMenu(main_frame, self.cutting_complexity_var, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10").grid(row=13, column=1, columnspan=2, padx=10, pady=5, sticky="w")

tk.Button(main_frame, text="Calculate Cost", command=self.calculate_and_save, font=("Arial", 12)).grid(row=14, column=0, columnspan=3, pady=10)

Footer
footer = tk.Frame(self.root)
footer.pack(side=tk.BOTTOM, fill=tk.X)
self.create_footer(footer)

def add_sub_part(self):
"""
Placeholder to add a sub-part to the assembly (FR2).
Logic:

Adds a dummy sub-part to the listbox.
Logs test result. """ sub_part_id = f"SUBPART-{len(self.sub_parts_listbox.get(0, tk.END)) + 1}" self.sub_parts_listbox.insert(tk.END, sub_part_id) messagebox.showinfo("Add Sub-Part", f"Added {sub_part_id} (details TBD)") log_test_result( test_case="FR2: Add sub-part", input_data="None", output=f"Added {sub_part_id} to listbox", pass_fail="Pass" )
def remove_sub_part(self):
"""
Remove a selected sub-part from the assembly (FR2).
Logic:

Removes the selected sub-part from the listbox.
Shows error if no selection.
Logs test result. """ selected = self.sub_parts_listbox.curselection() if selected: self.sub_parts_listbox.delete(selected) log_test_result( test_case="FR2: Remove sub-part", input_data=f"Index: {selected}", output="Sub-part removed", pass_fail="Pass" ) else: messagebox.showerror("Error", "Select a sub-part to remove") log_test_result( test_case="FR2: Remove sub-part", input_data="None", output="No sub-part selected", pass_fail="Fail" )
def calculate_and_save(self):
"""
Calculate cost and save output based on part specifications (FR2, FR3, FR4, FR5).

Logic:

Retrieves part specifications including cutting inputs.
Validates inputs.
Loads rates and calculates cost.
Saves result and navigates to quote screen. """ try: part_type = self.part_type_var.get() part_id = self.part_id_entry.get().strip() revision = self.revision_entry.get().strip() material = self.material_var.get().lower() thickness = self.thickness_var.get() # Dropdown value as string length = self.length_entry.get().strip() width = self.width_entry.get().strip() quantity = self.quantity_var.get() if quantity == "Other": quantity = self.custom_quantity_entry.get().strip() top_level_assembly = self.top_level_assembly_entry.get().strip() weldment_indicator = self.weldment_var.get() cutting_method = self.cutting_method_var.get() cutting_complexity = self.cutting_complexity_var.get() # Dropdown value as string
input_data = (f"Part Type: {part_type}, Part ID: {part_id}, Revision: {revision}, Material: {material}, "
f"Thickness: {thickness}, Length: {length}, Width: {width}, Quantity: {quantity}, "
f"Top-Level Assembly: {top_level_assembly}, Weldment: {weldment_indicator}, "
f"Cutting Method: {cutting_method}, Cutting Complexity: {cutting_complexity}")

if not all([part_id, revision, material, thickness, length, width, quantity]):
output = "All required fields must be filled"
messagebox.showerror("Error", output)
log_test_result(
test_case="FR2: Part input with empty fields",
input_data=input_data,
output=output,
pass_fail="Fail"
)
return

thickness = float(thickness)  # Convert dropdown string to float
length = float(length)
width = float(width)
quantity = int(quantity)
cutting_complexity = float(cutting_complexity) if cutting_method != "None" else 0.0

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
output = "Length must be between 50 and 3000 mm"
messagebox.showerror("Error", output)
log_test_result(
test_case="FR2: Invalid length",
input_data=input_data,
output=output,
pass_fail="Fail"
)
return
if not (50 <= width <= 1500):
output = "Width must be between 50 and 1500 mm"
messagebox.showerror("Error", output)
log_test_result(
test_case="FR2: Invalid width",
input_data=input_data,
output=output,
pass_fail="Fail"
)
return
if quantity <= 0:
output = "Quantity must be a positive integer"
messagebox.showerror("Error", output)
log_test_result(
test_case="FR2: Invalid quantity",
input_data=input_data,
output=output,
pass_fail="Fail"
)
return
if cutting_method != "None" and not (1 <= cutting_complexity <= 10):
output = "Cutting complexity must be between 1 and 10"
messagebox.showerror("Error", output)
log_test_result(
test_case="FR2.1: Invalid cutting complexity",
input_data=input_data,
output=output,
pass_fail="Fail"
)
return

part_specs = {
'part_type': part_type,
'part_id': part_id,
'revision': revision,
'material': material,
'thickness': thickness,
'length': length,
'width': width,
'quantity': quantity,
'top_level_assembly': top_level_assembly,
'weldment_indicator': weldment_indicator,
'cutting_method': cutting_method,
'cutting_complexity': cutting_complexity,
'sub_parts': [self.sub_parts_listbox.get(i) for i in range(self.sub_parts_listbox.size())]
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
output = "Invalid input: Length, width, quantity, and cutting complexity must be numeric"
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

Clears existing widgets.
Creates main content frame and footer.
Adds fields for customer name and profit margin, and generate quote button. """ self.clear_screen()
Main content
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

Footer
footer = tk.Frame(self.root)
footer.pack(side=tk.BOTTOM, fill=tk.X)
self.create_footer(footer)

def generate_quote(self, part_id, total_cost):
"""
Generate and save a quote (FR7).

Logic:

Retrieves customer name and profit margin from entry fields.
Validates inputs (non-empty customer name, numeric non-negative margin).
Calls save_quote to generate and save the quote to quotes.txt.
Logs test result to test_logs.txt using logger.
Shows success message.
Returns to part input screen. """ try: customer_name = self.customer_entry.get().strip() profit_margin = self.margin_entry.get().strip() input_data = f"Customer Name: {customer_name}, Profit Margin: {profit_margin}%"
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

Clears existing widgets.
Creates main content frame and footer.
Adds fields for rate key and value, update rate button, and user features button. """ self.clear_screen()
Main content
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

Footer
footer = tk.Frame(self.root)
footer.pack(side=tk.BOTTOM, fill=tk.X)
self.create_footer(footer)

def update_rate(self):
"""
Update a rate in rates_global.txt (FR6).

Logic:

Retrieves rate key and value from entry fields.
Validates inputs (non-empty key, numeric non-negative value).
Calls update_rates to save the new rate.
Logs test result to test_logs.txt using logger.
Shows success message. """ try: rate_key = self.rate_key_entry.get().strip() rate_value = self.rate_value_entry.get().strip() input_data = f"Rate Key: {rate_key}, Rate Value: {rate_value}"
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

Destroys all child widgets of the root window.
Used to switch between screens (e.g., login to part input). """ for widget in self.root.winfo_children(): widget.destroy()
if name == "main":
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
