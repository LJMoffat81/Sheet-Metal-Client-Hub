import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.parts = []
        # Other initialization code...

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_part_input_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Part Input", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)
        
        materials = ["CR4 Mild Steel", "304 Stainless Steel", "316 Stainless Steel", "5052 Aluminium", "6061 Aluminium", "6082 Aluminium", "S275 Structural Steel", "S355 Structural Steel", "3003 Aluminium", "Zinc Coated Mild Steel"]
        thicknesses = [1.0, 1.2, 1.5, 2.0, 2.5, 3.0]
        
        tk.Label(self.root, text="Material:", font=("Arial", 12), fg="blue").pack()
        material_var = tk.StringVar(value=materials[0])
        material_dropdown = tk.OptionMenu(self.root, material_var, *materials)
        material_dropdown.pack()
        
        tk.Label(self.root, text="Thickness (mm):", font=("Arial", 12), fg="blue").pack()
        thickness_var = tk.DoubleVar(value=1.0)
        thickness_dropdown = tk.OptionMenu(self.root, thickness_var, *thicknesses)
        thickness_dropdown.pack()
        
        tk.Label(self.root, text="Lay-flat Length (mm, 50-3000):", font=("Arial", 12), fg="blue").pack()
        length_entry = tk.Entry(self.root)
        length_entry.pack()
        
        tk.Label(self.root, text="Lay-flat Width (mm, 50-1500):", font=("Arial", 12), fg="blue").pack()
        width_entry = tk.Entry(self.root)
        width_entry.pack()
        
        tk.Label(self.root, text="Number of Bends (0-20):", font=("Arial", 12), fg="blue").pack()
        bends_entry = tk.Entry(self.root)
        bends_entry.pack()
        
        tk.Label(self.root, text="Cutting Required (Yes/No):", font=("Arial", 12), fg="blue").pack()
        cutting_var = tk.StringVar(value="No")
        cutting_dropdown = tk.OptionMenu(self.root, cutting_var, "Yes", "No")
        cutting_dropdown.pack()
        
        parts_listbox = tk.Listbox(self.root, width=50, font=("Arial", 12))
        parts_listbox.pack(pady=10)
        
        tk.Button(self.root, text="Add Part", command=lambda: self.add_part(material_var.get(), thickness_var.get(), length_entry.get(), width_entry.get(), bends_entry.get(), cutting_var.get(), parts_listbox, length_entry, width_entry, bends_entry), font=("Arial", 12), fg="blue", bg="grey").pack()
        tk.Button(self.root, text="Delete Part", command=lambda: self.delete_part(parts_listbox), font=("Arial", 12), fg="blue", bg="grey").pack()
        tk.Button(self.root, text="Calculate", command=self.show_cost_output_screen, font=("Arial", 12), fg="blue", bg="grey").pack()
        tk.Button(self.root, text="Settings", command=self.show_settings_screen, font=("Arial", 12), fg="blue", bg="grey").place(x=600, y=20)

    def add_part(self, material, thickness, length, width, bends, cutting, listbox, length_entry, width_entry, bends_entry):
        if not length or not width or not bends:
            messagebox.showerror("Error", "Length, width, and bends must be filled")
            return
        try:
            length = float(length)
            width = float(width)
            bends = int(bends)
        except ValueError:
            messagebox.showerror("Error", "Length, width, and bends must be numeric")
            return
        if thickness not in [1.0, 1.2, 1.5, 2.0, 2.5, 3.0]:
            messagebox.showerror("Error", "Thickness must be one of 1, 1.2, 1.5, 2, 2.5, 3 mm")
            return
        if not 50 <= length <= 3000:
            messagebox.showerror("Error", "Lay-flat length must be between 50 and 3000 mm")
            return
        if not 50 <= width <= 1500:
            messagebox.showerror("Error", "Lay-flat width must be between 50 and 1500 mm")
            return
        if not 0 <= bends <= 20:
            messagebox.showerror("Error", "Bends must be between 0 and 20")
            return
        part = {"material": material, "thickness": thickness, "length": length, "width": width, "bends": bends, "cutting": cutting}
        self.parts.append(part)
        listbox.insert(tk.END, f"{material}, {thickness}mm, {length}x{width}mm, {bends} bends, Cutting: {cutting}")
        length_entry.delete(0, tk.END)
        width_entry.delete(0, tk.END)
        bends_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Part added successfully")

    def delete_part(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No part selected")
            return
        index = selection[0]
        listbox.delete(index)
        self.parts.pop(index)
        messagebox.showinfo("Success", "Part deleted successfully")

    # Placeholder for other methods
    def show_cost_output_screen(self):
        pass

    def show_settings_screen(self):
        pass

    # Main block to run the GUI
    if __name__ == "__main__":
        root = tk.Tk()
        app = App(root)
        app.show_part_input_screen()
        root.mainloop()
