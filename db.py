import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Harish@123",   # your MySQL password
        database="student_enrollment"
    )
def get_dashboard_counts():
    con = get_connection()
    cursor = con.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM enrollments")
    enrollments = cursor.fetchone()[0]

    con.close()
    return students, courses, enrollments
