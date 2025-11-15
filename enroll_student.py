import customtkinter as ctk
from tkinter import messagebox
from db import get_connection


class EnrollWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.title("Enroll Student")
        self.geometry("450x420")
        self.resizable(False, False)

        # Title
        title = ctk.CTkLabel(self, text="Enroll Student to Course",
                             font=("Arial", 22, "bold"))
        title.pack(pady=25)

        # Frame
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(pady=10)

        # Combo: Students
        self.student_combo = ctk.CTkComboBox(
            form, values=[], width=300, state="readonly")
        self.student_combo.set("Select Student")
        self.student_combo.pack(pady=12)

        # Combo: Courses
        self.course_combo = ctk.CTkComboBox(
            form, values=[], width=300, state="readonly")
        self.course_combo.set("Select Course")
        self.course_combo.pack(pady=12)

        # Enroll Button
        enroll_btn = ctk.CTkButton(
            self, text="Enroll Student", width=260, command=self.enroll_student)
        enroll_btn.pack(pady=20)

        self.load_dropdowns()

    # Load data into dropdowns
    def load_dropdowns(self):
        try:
            con = get_connection()
            cursor = con.cursor()

            # Load students
            cursor.execute("SELECT student_id, full_name FROM students")
            students = cursor.fetchall()
            self.student_map = {name: sid for sid, name in students}
            self.student_combo.configure(values=list(self.student_map.keys()))

            # Load courses
            cursor.execute("SELECT course_id, course_name FROM courses")
            courses = cursor.fetchall()
            self.course_map = {name: cid for cid, name in courses}
            self.course_combo.configure(values=list(self.course_map.keys()))

            con.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def enroll_student(self):
        student_name = self.student_combo.get()
        course_name = self.course_combo.get()

        if student_name == "Select Student" or course_name == "Select Course":
            messagebox.showerror("Error", "Please select both student and course.")
            return

        sid = self.student_map[student_name]
        cid = self.course_map[course_name]

        try:
            con = get_connection()
            cursor = con.cursor()

            # Check duplicate
            cursor.execute("SELECT * FROM enrollments WHERE student_id=%s AND course_id=%s", (sid, cid))
            existing = cursor.fetchone()

            if existing:
                messagebox.showerror("Duplicate Enrollment", 
                                    f"{student_name} is already enrolled in {course_name}.")
                con.close()
                return

            # Insert enrollment
            sql = "INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)"
            cursor.execute(sql, (sid, cid))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Enrollment successful!")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

