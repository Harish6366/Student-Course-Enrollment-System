import customtkinter as ctk
from tkinter import messagebox
from db import get_connection


class ManageStudents(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.title("Manage Students")
        self.geometry("900x600")
        self.resizable(True, True)

        # Title
        title = ctk.CTkLabel(self, text="Manage Students",
                             font=("Arial", 24, "bold"))
        title.pack(pady=12)

        # Search Bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=12)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search student name...", width=350)
        self.search_entry.pack(side="left", padx=10, pady=10)

        search_btn = ctk.CTkButton(search_frame, text="Search", width=120, command=self.search_students)
        search_btn.pack(side="left", padx=5)

        refresh_btn = ctk.CTkButton(search_frame, text="Refresh", width=120, command=self.load_students)
        refresh_btn.pack(side="left", padx=5)

        # Table Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(10, 2))

        headers = ["ID", "Name", "Email", "Department", "Year", "Actions"]
        widths = [60, 200, 220, 150, 80, 120]

        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(header_frame, text=h, width=widths[i], anchor="w", font=("Arial", 15, "bold"))
            lbl.pack(side="left", padx=5)

        # Scrollable list
        self.table = ctk.CTkScrollableFrame(self, width=860, height=420)
        self.table.pack(padx=12, pady=10, fill="both", expand=True)

        self.row_widgets = []

        # load rows
        self.load_students()

    def clear_rows(self):
        for w in self.row_widgets:
            w.destroy()
        self.row_widgets.clear()

    def load_students(self):
        self.clear_rows()
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            con.close()

            for row in rows:
                self.add_row(row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def add_row(self, row_data):
        row_frame = ctk.CTkFrame(self.table, fg_color="transparent")
        row_frame.pack(fill="x", pady=4)

        student_id, name, email, dept, year = row_data

        widths = [60, 200, 220, 150, 80]

        values = [student_id, name, email, dept, year]

        for i, val in enumerate(values):
            lbl = ctk.CTkLabel(row_frame, text=str(val), width=widths[i], anchor="w", font=("Arial", 14))
            lbl.pack(side="left", padx=4)

        # Action Buttons
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.pack(side="left")

        edit_btn = ctk.CTkButton(action_frame, text="Edit", width=55,
                                 command=lambda: EditStudentWindow(row_data, self))
        edit_btn.pack(side="left", padx=3)

        delete_btn = ctk.CTkButton(action_frame, text="Delete", fg_color="red", width=55,
                                   command=lambda: self.delete_student(student_id))
        delete_btn.pack(side="left", padx=3)

        self.row_widgets.append(row_frame)

    def delete_student(self, sid):
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?"):
            return

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
            con.commit()
            con.close()

            messagebox.showinfo("Deleted", "Student deleted successfully.")
            self.load_students()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_students(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Empty", "Enter a search term.")
            return

        self.clear_rows()

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM students WHERE full_name LIKE %s", (f"%{keyword}%",))
            rows = cursor.fetchall()
            con.close()

            for row in rows:
                self.add_row(row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))


# --- EDIT WINDOW ---
class EditStudentWindow(ctk.CTkToplevel):
    def __init__(self, student_row, parent):
        super().__init__()

        self.parent = parent
        sid, name, email, dept, year = student_row

        self.title("Edit Student")
        self.geometry("400x450")
        self.resizable(False, False)

        title = ctk.CTkLabel(self, text="Edit Student", font=("Arial", 22, "bold"))
        title.pack(pady=25)

        self.sid = sid

        # Entries
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Full Name", width=300)
        self.name_entry.insert(0, name)
        self.name_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=300)
        self.email_entry.insert(0, email)
        self.email_entry.pack(pady=10)

        self.dept_entry = ctk.CTkEntry(self, placeholder_text="Department", width=300)
        self.dept_entry.insert(0, dept)
        self.dept_entry.pack(pady=10)

        self.year_entry = ctk.CTkEntry(self, placeholder_text="Year", width=300)
        self.year_entry.insert(0, str(year))
        self.year_entry.pack(pady=10)

        save_btn = ctk.CTkButton(self, text="Save Changes", width=250, command=self.save_changes)
        save_btn.pack(pady=20)

    def save_changes(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        dept = self.dept_entry.get().strip()
        year = self.year_entry.get().strip()

        if not all([name, email, dept, year]):
            messagebox.showerror("Error", "All fields required.")
            return

        try:
            con = get_connection()
            cursor = con.cursor()
            sql = """
            UPDATE students
            SET full_name=%s, email=%s, department=%s, year_of_study=%s
            WHERE student_id=%s
            """
            cursor.execute(sql, (name, email, dept, year, self.sid))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Student updated successfully.")
            self.destroy()
            self.parent.load_students()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
