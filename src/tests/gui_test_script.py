import sys
import os
# Add the parent directory (src/) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gui import SheetMetalClientHub
import tkinter as tk

# Create the main window and run the application
root = tk.Tk()
app = SheetMetalClientHub(root)
root.mainloop()

def automate_gui():
    root = tk.Tk()
    app = SheetMetalClientHub(root)

    # Login
    app.username_entry.insert(0, 'laurin')
    app.password_entry.insert(0, 'moffat123')
    app.login()
    time.sleep(0.5)

    # Create part input
    app.notebook.select(1)
    app.part_id_entry.delete(0, tk.END)
    app.part_id_entry.insert(0, 'PART-67890ABCDE')
    app.revision_entry.insert(0, 'A')
    app.single_material_var.set('Mild Steel')
    app.single_thickness_var.set('1.0')
    app.single_lay_flat_length_var.set('1000')
    app.single_lay_flat_width_var.set('500')
    app.single_quantity_var.set('10')
    app.work_centre_vars[0].set('Welding')
    app.work_centre_quantity_vars[0].set('100')
    app.work_centre_sub_option_vars[0].set('MIG')
    app.calculate_and_save()
    time.sleep(0.5)

    # Generate quote
    app.create_quote_screen('PART-67890ABCDE', 50.0)
    app.customer_entry.insert(0, 'Acme Corp')
    app.margin_entry.insert(0, '20')
    app.generate_quote('PART-67890ABCDE', 50.0)
    time.sleep(0.5)

    root.destroy()

if __name__ == "__main__":
    automate_gui()