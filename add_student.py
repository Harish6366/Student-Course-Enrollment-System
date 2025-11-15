import customtkinter as ctk
from tkinter import messagebox
from db import get_connection


class AddStudentWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))


        self.title("Add Student")
        self.geometry("400x480")
        self.resizable(False, False)

        # Title
        title = ctk.CTkLabel(self, text="Add New Student", 
                             font=("Arial", 22, "bold"))
        title.pack(pady=20)

        # Form Frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10)

        # Full Name
        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Full Name", width=300)
        self.name_entry.pack(pady=10)

        # Email
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="Email Address", width=300)
        self.email_entry.pack(pady=10)

        # Department
        self.dept_entry = ctk.CTkEntry(form_frame, placeholder_text="Department (e.g., CSE)", width=300)
        self.dept_entry.pack(pady=10)

        # Year of Study
        self.year_entry = ctk.CTkEntry(form_frame, placeholder_text="Year of Study (1-4)", width=300)
        self.year_entry.pack(pady=10)

        # Save Button
        add_button = ctk.CTkButton(self, text="Save Student", width=250, command=self.save_student)
        add_button.pack(pady=20)

    # Save student to DB
    def save_student(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        dept = self.dept_entry.get().strip()
        year = self.year_entry.get().strip()

        if not name or not email or not dept or not year:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            con = get_connection()
            cursor = con.cursor()

            sql = "INSERT INTO students (full_name, email, department, year_of_study) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, dept, year))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Student added successfully!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
