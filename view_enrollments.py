import customtkinter as ctk
from db import get_connection
from tkinter import messagebox
from datetime import datetime
import openpyxl
from openpyxl.styles import Font
from tkinter.filedialog import asksaveasfilename

# Helper to safely format date strings to YYYY-MM-DD (or return None)
def _parse_date(s):
    s = s.strip()
    if not s:
        return None
    try:
        # accept yyyy-mm-dd or dd/mm/yyyy
        if "-" in s:
            dt = datetime.strptime(s, "%Y-%m-%d")
        elif "/" in s:
            dt = datetime.strptime(s, "%d/%m/%Y")
        else:
            # try ymd without separators
            dt = datetime.strptime(s, "%Y%m%d")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


class ViewEnrollmentsWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))

        self.title("View Enrollments")
        self.geometry("900x600")
        self.resizable(True, True)

        # Title
        title = ctk.CTkLabel(self, text="All Enrollments",
                             font=("Arial", 24, "bold"))
        title.pack(pady=12)

        # --- Filter Frame ---
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=12, pady=(0, 8))

        # Student search
        self.student_search = ctk.CTkEntry(filter_frame, placeholder_text="Search student name (partial)", width=300)
        self.student_search.grid(row=0, column=0, padx=8, pady=8, sticky="w")

        # Course search
        self.course_search = ctk.CTkEntry(filter_frame, placeholder_text="Search course name (partial)", width=300)
        self.course_search.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        # Date from
        self.date_from = ctk.CTkEntry(filter_frame, placeholder_text="Date from (YYYY-MM-DD or DD/MM/YYYY)", width=260)
        self.date_from.grid(row=1, column=0, padx=8, pady=6, sticky="w")

        # Date to
        self.date_to = ctk.CTkEntry(filter_frame, placeholder_text="Date to (YYYY-MM-DD or DD/MM/YYYY)", width=260)
        self.date_to.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        # Buttons: Search, Clear
        btn_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, rowspan=2, padx=8, pady=8, sticky="n")

        search_btn = ctk.CTkButton(btn_frame, text="Search / Filter", width=160, command=self.on_search)
        search_btn.pack(padx=6, pady=(8,6))

        clear_btn = ctk.CTkButton(btn_frame, text="Clear / Refresh", width=160, command=self.on_clear)
        clear_btn.pack(padx=6, pady=(6,8))
        export_btn = ctk.CTkButton(btn_frame, text="Export to Excel", width=160, command=self.export_excel)
        export_btn.pack(padx=6, pady=6)


        # --- Table headers ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=12, pady=(2,4))

        headers = ["ID", "Student Name", "Course Name", "Enrollment Date"]
        widths = [60, 320, 320, 180]
        for i, h in enumerate(headers):
            lbl = ctk.CTkLabel(header_frame, text=h, width=widths[i], anchor="w", font=("Arial", 14, "bold"))
            lbl.pack(side="left", padx=6)

        # --- Scrollable container for rows ---
        self.table_frame = ctk.CTkScrollableFrame(self, width=860, height=400)
        self.table_frame.pack(padx=12, pady=6, fill="both", expand=True)

        # Keep references to displayed rows so we can clear them
        self._row_widgets = []

        # initial load
        self.load_rows()

    def _clear_rows(self):
        for w in self._row_widgets:
            w.destroy()
        self._row_widgets = []

    def load_rows(self, filters=None):
        """
        Load enrollments from DB.
        filters: dict with optional keys: student_like, course_like, date_from, date_to
        """
        try:
            con = get_connection()
            cursor = con.cursor()

            base_sql = """
            SELECT e.enrollment_id, s.full_name, c.course_name, e.enrollment_date
            FROM enrollments e
            JOIN students s ON s.student_id = e.student_id
            JOIN courses c ON c.course_id = e.course_id
            """

            conditions = []
            params = []

            if filters:
                if filters.get("student_like"):
                    conditions.append("s.full_name LIKE %s")
                    params.append(f"%{filters['student_like']}%")
                if filters.get("course_like"):
                    conditions.append("c.course_name LIKE %s")
                    params.append(f"%{filters['course_like']}%")
                if filters.get("date_from"):
                    conditions.append("e.enrollment_date >= %s")
                    params.append(filters["date_from"])
                if filters.get("date_to"):
                    conditions.append("e.enrollment_date <= %s")
                    params.append(filters["date_to"])

            if conditions:
                base_sql += " WHERE " + " AND ".join(conditions)

            base_sql += " ORDER BY e.enrollment_id DESC"

            cursor.execute(base_sql, tuple(params))
            rows = cursor.fetchall()
            con.close()

            # clear previous
            self._clear_rows()

            # add rows
            for row in rows:
                self._add_row(row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def _add_row(self, row_data):
        # A single row container
        row = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        row.pack(fill="x", padx=6, pady=3)

        # Columns
        widths = [60, 320, 320, 180]
        for i, data in enumerate(row_data):
            lbl = ctk.CTkLabel(row, text=str(data), width=widths[i], anchor="w", font=("Arial", 13))
            lbl.pack(side="left", padx=(4,6))

        self._row_widgets.append(row)

    # Button callbacks
    def on_search(self):
        s = self.student_search.get().strip()
        c = self.course_search.get().strip()
        df_raw = self.date_from.get().strip()
        dt_raw = self.date_to.get().strip()

        df = _parse_date(df_raw) if df_raw else None
        dt = _parse_date(dt_raw) if dt_raw else None

        if (df_raw and not df) or (dt_raw and not dt):
            messagebox.showerror("Date format error", "Please enter dates as YYYY-MM-DD or DD/MM/YYYY")
            return

        filters = {}
        if s:
            filters["student_like"] = s
        if c:
            filters["course_like"] = c
        if df:
            filters["date_from"] = df
        if dt:
            filters["date_to"] = dt

        self.load_rows(filters)

    def on_clear(self):
        # clear inputs
        self.student_search.delete(0, "end")
        self.course_search.delete(0, "end")
        self.date_from.delete(0, "end")
        self.date_to.delete(0, "end")

        # reload all rows
        self.load_rows()
    def export_excel(self):
    

        # ask where to save the file
        filepath = asksaveasfilename(defaultextension=".xlsx",
                                    filetypes=[("Excel Files", "*.xlsx")],
                                    title="Save Enrollments As")
        if not filepath:
            return

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute("""
                SELECT e.enrollment_id, s.full_name, c.course_name, e.enrollment_date
                FROM enrollments e
                JOIN students s ON s.student_id = e.student_id
                JOIN courses c ON c.course_id = e.course_id
                ORDER BY e.enrollment_id DESC
            """)
            rows = cursor.fetchall()
            con.close()

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Enrollments"

            headers = ["ID", "Student Name", "Course Name", "Enrollment Date"]
            ws.append(headers)

            # Style headers
            for col in range(1, len(headers) + 1):
                ws.cell(row=1, column=col).font = Font(bold=True)

            # Add data
            for row in rows:
                ws.append(row)

            wb.save(filepath)

            messagebox.showinfo("Success", f"Exported to:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

