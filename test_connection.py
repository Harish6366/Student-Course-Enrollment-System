from db import get_connection

try:
    con = get_connection()
    print("Connected successfully!")
    con.close()
except Exception as e:
    print("Connection failed:", e)
