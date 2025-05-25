import tkinter as tk
from tkinter import messagebox
from file_handler import FileHandler  # Import the class

class SheetMetalClientHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Sheet Metal Client Hub")
        self.file_handler = FileHandler()  # Create an instance
        self.role = None
        self.setup_login()

    def setup_login(self):
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.file_handler.validate_credentials(username, password):  # Use instance method
            self.role = "User"  # Simplified for example
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid credentials")

if __name__ == "__main__":
    root = tk.Tk()
    app = SheetMetalClientHub(root)
    root.mainloop()
