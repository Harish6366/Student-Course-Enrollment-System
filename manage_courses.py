import customtkinter as ctk
from tkinter import messagebox
from db import get_connection


class ManageCourses(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.title("Manage Courses")
        self.geometry("900x550")
        self.resizable(True, True)

        title = ctk.CTkLabel(self, text="Manage Courses",
                             font=("Arial", 24, "bold"))
        title.pack(pady=15)

        # Search Bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=12)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search course name...", width=350)
        self.search_entry.pack(side="left", padx=10, pady=10)

        search_btn = ctk.CTkButton(search_frame, text="Search", width=120, command=self.search_courses)
        search_btn.pack(side="left", padx=5)

        refresh_btn = ctk.CTkButton(search_frame, text="Refresh", width=120, command=self.load_courses)
        refresh_btn.pack(side="left", padx=5)

        # Table Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(10, 2))

        headers = ["ID", "Course Name", "Credits", "Actions"]
        widths = [80, 420, 120, 150]

        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(header_frame, text=h, width=widths[i], anchor="w", font=("Arial", 15, "bold"))
            lbl.pack(side="left", padx=6)

        # Scrollable list
        self.table = ctk.CTkScrollableFrame(self, width=850, height=380)
        self.table.pack(padx=12, pady=10, fill="both", expand=True)

        self.row_widgets = []

        self.load_courses()

    def clear_rows(self):
        for w in self.row_widgets:
            w.destroy()
        self.row_widgets.clear()

    def load_courses(self):
        self.clear_rows()

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()
            con.close()

            for row in rows:
                self.add_row(row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def add_row(self, row_data):
        course_id, name, credits = row_data

        row_frame = ctk.CTkFrame(self.table, fg_color="transparent")
        row_frame.pack(fill="x", pady=4)

        widths = [80, 420, 120]

        values = [course_id, name, credits]

        for i, val in enumerate(values):
            lbl = ctk.CTkLabel(row_frame, text=str(val), width=widths[i], anchor="w", font=("Arial", 14))
            lbl.pack(side="left", padx=(5, 10))

        # Action buttons
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.pack(side="left")

        edit_btn = ctk.CTkButton(action_frame, text="Edit", width=65,
                                 command=lambda: EditCourseWindow(row_data, self))
        edit_btn.pack(side="left", padx=6)

        delete_btn = ctk.CTkButton(action_frame, text="Delete", width=65, fg_color="red",
                                   command=lambda: self.delete_course(course_id))
        delete_btn.pack(side="left", padx=6)

        self.row_widgets.append(row_frame)

    def delete_course(self, cid):
        if not messagebox.askyesno("Confirm Delete", "Delete this course?"):
            return

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("DELETE FROM courses WHERE course_id=%s", (cid,))
            con.commit()
            con.close()

            messagebox.showinfo("Deleted", "Course deleted successfully.")
            self.load_courses()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def search_courses(self):
        keyword = self.search_entry.get().strip()
        if not keyword:
            messagebox.showwarning("Empty", "Enter a search term.")
            return

        self.clear_rows()

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM courses WHERE course_name LIKE %s", (f"%{keyword}%",))
            rows = cursor.fetchall()
            con.close()

            for row in rows:
                self.add_row(row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))


# --- EDIT WINDOW FOR COURSES ---
class EditCourseWindow(ctk.CTkToplevel):
    def __init__(self, course_row, parent):
        super().__init__()

        self.parent = parent
        cid, name, credits = course_row

        self.cid = cid

        self.title("Edit Course")
        self.geometry("400x350")
        self.resizable(False, False)

        title = ctk.CTkLabel(self, text="Edit Course", font=("Arial", 22, "bold"))
        title.pack(pady=25)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Course Name", width=300)
        self.name_entry.insert(0, name)
        self.name_entry.pack(pady=10)

        self.credits_entry = ctk.CTkEntry(self, placeholder_text="Credits", width=300)
        self.credits_entry.insert(0, str(credits))
        self.credits_entry.pack(pady=10)

        save_btn = ctk.CTkButton(self, text="Save Changes", width=250, command=self.save_changes)
        save_btn.pack(pady=20)

    def save_changes(self):
        name = self.name_entry.get().strip()
        credits = self.credits_entry.get().strip()

        if not name or not credits:
            messagebox.showerror("Error", "All fields required.")
            return

        if not credits.isdigit():
            messagebox.showerror("Error", "Credits must be a number.")
            return

        try:
            con = get_connection()
            cursor = con.cursor()
            sql = """
            UPDATE courses
            SET course_name=%s, credits=%s
            WHERE course_id=%s
            """
            cursor.execute(sql, (name, credits, self.cid))
            con.commit()
            con.close()

            messagebox.showinfo("Success", "Course updated successfully.")
            self.destroy()
            self.parent.load_courses()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
