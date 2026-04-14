from datetime import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
#import plotly.express as px

conn = sqlite3.connect("company.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# ===================== TABLES =====================

cursor.execute("""
CREATE TABLE IF NOT EXISTS Department (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    department_id INTEGER,
    salary INTEGER,
    join_date TEXT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id INTEGER,
    date TEXT,
    status TEXT,
    working_hours INTEGER,
    FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
)
""")

conn.commit()

# ===================== BASIC FUNCTIONS =====================

def add_department():
    name = input("Enter Department Name: ")
    cursor.execute("INSERT INTO Department (department_name) VALUES (?)", (name,))
    conn.commit()
    print("✅ Department Added")

def view_departments():
    df = pd.read_sql_query("SELECT * FROM Department", conn)
    print(df)

def add_employee():
    name = input("Enter Name: ")

    while True:
        try:
            age = int(input("Enter Age: "))
            if age > 18:
                break
        except:
            print("Invalid age")

    while True:
        try:
            dept_id = int(input("Enter Department ID: "))
            cursor.execute("SELECT * FROM Department WHERE department_id=?", (dept_id,))
            if cursor.fetchone():
                break
            print("Department not found")
        except:
            print("Invalid input")

    while True:
        try:
            salary = int(input("Enter Salary: "))
            if salary > 0:
                break
        except:
            print("Invalid salary")

    while True:
        date = input("Enter Join Date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except:
            print("Invalid date")

    cursor.execute("""
    INSERT INTO Employees (name, age, department_id, salary, join_date)
    VALUES (?, ?, ?, ?, ?)
    """, (name, age, dept_id, salary, date))

    conn.commit()
    print("✅ Employee Added")

def view_employees():
    df = pd.read_sql_query("""
    SELECT e.emp_id, e.name, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    """, conn)
    print(df)

def search_employee():
    name = input("Enter name: ")
    df = pd.read_sql_query(f"""
    SELECT e.emp_id, e.name, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    WHERE e.name LIKE '%{name}%'
    """, conn)
    print(df)

def update_employee():
    emp_id = input("Enter ID: ")
    salary = int(input("Enter new salary: "))
    cursor.execute("UPDATE Employees SET salary=? WHERE emp_id=?", (salary, emp_id))
    conn.commit()
    print("Updated")

def delete_employee():
    emp_id = input("Enter ID: ")
    cursor.execute("DELETE FROM Employees WHERE emp_id=?", (emp_id,))
    conn.commit()
    print("Deleted")

# ===================== ANALYTICS =====================

def show_data_table():
    df = pd.read_sql_query("""
    SELECT e.emp_id, e.name, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    """, conn)
    print(df)

def salary_graph():
    df = pd.read_sql_query("SELECT name, salary FROM Employees", conn)
    plt.figure()
    plt.bar(df["name"], df["salary"])
    plt.xticks(rotation=45)
    plt.title("Employee Salary")
    plt.show()

def seaborn_graph():
    df = pd.read_sql_query("""
    SELECT d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    """, conn)
    sns.barplot(x="department_name", y="salary", data=df)
    plt.xticks(rotation=45)
    plt.title("Department vs Salary")
    plt.show()

def plotly_graph():
    df = pd.read_sql_query("""
    SELECT e.name, e.salary, d.department_name
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    """, conn)
    fig = px.bar(df, x="name", y="salary", color="department_name")
    fig.show()

def attendance_graph():
    df = pd.read_sql_query("""
    SELECT status, COUNT(*) as count
    FROM Attendance
    GROUP BY status
    """, conn)
    plt.figure()
    plt.pie(df["count"], labels=df["status"], autopct='%1.1f%%')
    plt.title("Attendance Report")
    plt.show()

# ===================== MENU =====================

while True:
    print("\n--- EMPLOYEE MANAGEMENT SYSTEM ---")
    print("1. Add Department")
    print("2. View Departments")
    print("3. Add Employee")
    print("4. View Employees")
    print("5. Search Employee")
    print("6. Update Employee")
    print("7. Delete Employee")
    print("8. Show Data Table (Pandas)")
    print("9. Salary Graph (Matplotlib)")
    print("10. Department Graph (Seaborn)")
    print("11. Interactive Graph (Plotly)")
    print("12. Attendance Graph")
    print("13. Exit")

    choose = int(input("Enter choice: "))

    if choose == "1": add_department()
    elif choose == "2": view_departments()
    elif choose == "3": add_employee()
    elif choose == "4": view_employees()
    elif choose == "5": search_employee()
    elif choose == "6": update_employee()
    elif choose == "7": delete_employee()
    elif choose == "8": show_data_table()
    elif choose == "9": salary_graph()
    elif choose == "10": seaborn_graph()
    elif choose == "11": plotly_graph()
    elif choose == "12": attendance_graph()
    elif choose == "13":
        break
    else:
        print("Invalid choice")

conn.close()
print("Application Closed")