import customtkinter as ctk
from add_student import AddStudentWindow
from add_course import AddCourseWindow
from enroll_student import EnrollWindow
from view_enrollments import ViewEnrollmentsWindow
from manage_students import ManageStudents
from manage_courses import ManageCourses
from db import get_dashboard_counts


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        # Theme Switch (Light / Dark)
        self.theme_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(pady=5)


        self.title("Student Enrollment System")
        self.geometry("600x650")

        # MAIN TITLE
        title = ctk.CTkLabel(self, text="Dashboard",
                             font=("Arial", 28, "bold"))
        title.pack(pady=20)

        # --- STATS CARD SECTION ---
        stats = get_dashboard_counts()
        total_students, total_courses, total_enrollments = stats

        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=10)

        # Card 1
        card1 = ctk.CTkFrame(stats_frame, width=150, height=120, corner_radius=15)
        card1.pack(side="left", padx=10)

        c1_label = ctk.CTkLabel(card1, text="Students", font=("Arial", 16, "bold"))
        c1_label.pack(pady=(15, 5))

        c1_value = ctk.CTkLabel(card1, text=str(total_students),
                                font=("Arial", 28, "bold"))
        c1_value.pack()

        # Card 2
        card2 = ctk.CTkFrame(stats_frame, width=150, height=120, corner_radius=15)
        card2.pack(side="left", padx=10)

        c2_label = ctk.CTkLabel(card2, text="Courses", font=("Arial", 16, "bold"))
        c2_label.pack(pady=(15, 5))

        c2_value = ctk.CTkLabel(card2, text=str(total_courses),
                                font=("Arial", 28, "bold"))
        c2_value.pack()

        # Card 3
        card3 = ctk.CTkFrame(stats_frame, width=150, height=120, corner_radius=15)
        card3.pack(side="left", padx=10)

        c3_label = ctk.CTkLabel(card3, text="Enrollments", font=("Arial", 16, "bold"))
        c3_label.pack(pady=(15, 5))

        c3_value = ctk.CTkLabel(card3, text=str(total_enrollments),
                                font=("Arial", 28, "bold"))
        c3_value.pack()

        # --- MENU BUTTONS ---
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=30)

        btn1 = ctk.CTkButton(frame, text="Add Student", width=250,
                             command=lambda: AddStudentWindow())
        btn1.pack(pady=10)

        btn2 = ctk.CTkButton(frame, text="Add Course", width=250,
                             command=lambda: AddCourseWindow())
        btn2.pack(pady=10)

        btn3 = ctk.CTkButton(frame, text="Enroll Student", width=250,
                             command=lambda: EnrollWindow())
        btn3.pack(pady=10)

        btn4 = ctk.CTkButton(frame, text="View Enrollments", width=250,
                             command=lambda: ViewEnrollmentsWindow())
        btn4.pack(pady=10)

        btn5 = ctk.CTkButton(frame, text="Manage Students", width=250,
                             command=lambda: ManageStudents())
        btn5.pack(pady=10)

        btn6 = ctk.CTkButton(frame, text="Manage Courses", width=250,
                             command=lambda: ManageCourses())
        btn6.pack(pady=10)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

        

# main is launched from login.py

