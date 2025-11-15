import customtkinter as ctk
from tkinter import messagebox
from main import MainApp   # open main window after login


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.title("Admin Login")
        self.geometry("400x350")
        self.resizable(False, False)

        title = ctk.CTkLabel(self, text="Admin Login",
                             font=("Arial", 26, "bold"))
        title.pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=280)
        self.username_entry.pack(pady=12)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", width=280, show="*")
        self.password_entry.pack(pady=12)

        login_btn = ctk.CTkButton(self, text="Login", width=200,
                                  command=self.verify_login)
        login_btn.pack(pady=20)

        self.admin_username = "admin"
        self.admin_password = "admin123"   # You can customize this

    def verify_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == self.admin_username and password == self.admin_password:
            messagebox.showinfo("Success", "Login Successful!")
            self.destroy()
            app = MainApp()   # open dashboard
            app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password.")
