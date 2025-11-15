import customtkinter as ctk
from tkinter import messagebox
from db import get_connection


class AddCourseWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))


        self.title("Add Course")
        self.geometry("400x350")
        self.resizable(False, False)

        # Title
        title = ctk.CTkLabel(self, text="Add New Course",
                             font=("Arial", 22, "bold"))
        title.pack(pady=30)

        # Form Frame
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10)

        # Course Name
        self.course_name_entry = ctk.CTkEntry(form_frame, placeholder_text="Course Name", width=300)
        self.course_name_entry.pack(pady=10)

        # Credits
        self.credits_entry = ctk.CTkEntry(form_frame, placeholder_text="Credits (e.g., 3 or 4)", width=300)
        self.credits_entry.pack(pady=10)

        # Save Button
        save_button = ctk.CTkButton(self, text="Save Course", width=250, command=self.save_course)
        save_button.pack(pady=20)

    # Save to DB
    def save_course(self):
        course_name = self.course_name_entry.get().strip()
        credits = self.credits_entry.get().strip()

        if not course_name or not credits:
            messagebox.showerror("Error", "All fields are required!")
            return

        if not credits.isdigit():
            messagebox.showerror("Error", "Credits must be a number!")
            return

        try:
            con = get_connection()
            cursor = con.cursor()

            sql = "INSERT INTO courses (course_name, credits) VALUES (%s, %s)"
            cursor.execute(sql, (course_name, credits))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Course added successfully!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
