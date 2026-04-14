from datetime import datetime
import sqlite3

conn = sqlite3.connect("company.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# ===================== DEPARTMENT =====================

cursor.execute("""
CREATE TABLE IF NOT EXISTS Department (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT
)
""")
conn.commit()


def add_department():
    name = input("Enter Department Name: ")
    cursor.execute("INSERT INTO Department (department_name) VALUES (?)", (name,))
    conn.commit()
    print("✅ Department Added")


def view_departments():
    cursor.execute("SELECT * FROM Department")
    rows = cursor.fetchall()
    if not rows:
        print("No departments found")
    else:
        print("\n--- Departments ---")
        for r in rows:
            print(f"ID: {r[0]}, Name: {r[1]}")


# ===================== EMPLOYEE =====================

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
conn.commit()


def add_employee():
    name = input("Enter Name: ")

    while True:
        try:
            age = int(input("Enter Age: "))
            if age > 18:
                break
            print("Age must be > 18")
        except:
            print("Invalid input")

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
            print("Salary must be > 0")
        except:
            print("Invalid input")

    while True:
        date = input("Enter Join Date (YYYY-MM-DD): ")
        try:
            d = datetime.strptime(date, "%Y-%m-%d")
            if d <= datetime.now():
                break
            print("Future date not allowed")
        except:
            print("Invalid format")

    cursor.execute("""
    INSERT INTO Employees (name, age, department_id, salary, join_date)
    VALUES (?, ?, ?, ?, ?)
    """, (name, age, dept_id, salary, date))

    conn.commit()
    print("✅ Employee Added")


def view_employees():
    cursor.execute("""
    SELECT e.emp_id, e.name, e.age, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    """)
    rows = cursor.fetchall()

    if not rows:
        print("No employees found")
    else:
        for r in rows:
            print("-" * 30)
            print(f"ID: {r[0]}")
            print(f"Name: {r[1]}")
            print(f"Age: {r[2]}")
            print(f"Department: {r[3]}")
            print(f"Salary: ₹{r[4]}")


def search_employee():
    name = input("Enter name to search: ")

    cursor.execute("""
    SELECT e.emp_id, e.name, e.age, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    WHERE e.name LIKE ?
    """, ('%' + name + '%',))

    rows = cursor.fetchall()

    if not rows:
        print("No employees found")
    else:
        for r in rows:
            print("-" * 30)
            print(f"ID: {r[0]}")
            print(f"Name: {r[1]}")
            print(f"Age: {r[2]}")
            print(f"Department: {r[3]}")
            print(f"Salary: ₹{r[4]}")


def update_employee():
    emp_id = input("Enter Employee ID: ")

    while True:
        try:
            salary = int(input("Enter New Salary: "))
            if salary > 0:
                break
            print("Invalid salary")
        except:
            print("Invalid input")

    cursor.execute("UPDATE Employees SET salary=? WHERE emp_id=?", (salary, emp_id))
    conn.commit()
    print("✅ Salary Updated")


def delete_employee():
    emp_id = input("Enter Employee ID: ")
    cursor.execute("DELETE FROM Employees WHERE emp_id=?", (emp_id,))
    conn.commit()
    print("🗑 Employee Deleted")


# ===================== SORT =====================

def sort_employees():
    print("1. Salary Low→High")
    print("2. Salary High→Low")
    print("3. Name A→Z")
    print("4. Name Z→A")

    choice = input("Choose: ")

    if choice == "1":
        order = "e.salary ASC"
    elif choice == "2":
        order = "e.salary DESC"
    elif choice == "3":
        order = "e.name ASC"
    elif choice == "4":
        order = "e.name DESC"
    else:
        print("Invalid choice")
        return

    cursor.execute(f"""
    SELECT e.emp_id, e.name, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    ORDER BY {order}
    """)

    rows = cursor.fetchall()

    for r in rows:
        print("-" * 30)
        print(f"ID: {r[0]}, Name: {r[1]}, Dept: {r[2]}, Salary: ₹{r[3]}")


# ===================== FILTER =====================

def filter_employees():
    while True:
        try:
            min_salary = int(input("Enter minimum salary: "))
            if min_salary > 0:
                break
            print("Invalid salary")
        except:
            print("Invalid input")

    cursor.execute("""
    SELECT e.emp_id, e.name, d.department_name, e.salary
    FROM Employees e
    JOIN Department d ON e.department_id = d.department_id
    WHERE e.salary > ?
    """, (min_salary,))

    rows = cursor.fetchall()

    for r in rows:
        print("-" * 30)
        print(f"ID: {r[0]}, Name: {r[1]}, Dept: {r[2]}, Salary: ₹{r[3]}")


# ===================== ATTENDANCE =====================

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


def mark_attendance():
    while True:
        try:
            emp_id = int(input("Enter Employee ID: "))
            cursor.execute("SELECT * FROM Employees WHERE emp_id=?", (emp_id,))
            if cursor.fetchone():
                break
            print("Employee not found")
        except:
            print("Invalid input")

    while True:
        date = input("Enter date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except:
            print("Invalid format")

    cursor.execute("SELECT * FROM Attendance WHERE emp_id=? AND date=?", (emp_id, date))
    if cursor.fetchone():
        print("Already marked")
        return

    status = input("Enter status (Present/Absent): ")

    if status.lower() == "present":
        hours = int(input("Enter working hours: "))
    else:
        hours = 0

    cursor.execute("""
    INSERT INTO Attendance (emp_id, date, status, working_hours)
    VALUES (?, ?, ?, ?)
    """, (emp_id, date, status, hours))

    conn.commit()
    print("✅ Attendance marked")


def view_attendance():
    cursor.execute("""
    SELECT e.name, a.date, a.status, a.working_hours
    FROM Attendance a
    JOIN Employees e ON a.emp_id = e.emp_id
    """)

    rows = cursor.fetchall()

    for r in rows:
        print("-" * 30)
        print(f"Name: {r[0]}, Date: {r[1]}, Status: {r[2]}, Hours: {r[3]}")


def attendance_report():
    cursor.execute("SELECT status, COUNT(*) FROM Attendance GROUP BY status")
    rows = cursor.fetchall()

    print("\n--- Attendance Summary ---")
    for r in rows:
        print(f"{r[0]}: {r[1]}")


def employee_monthly_attendance():
    emp_id = int(input("Enter Employee ID: "))
    month = input("Enter month (YYYY-MM): ")

    cursor.execute("""
    SELECT e.name, a.date, a.status
    FROM Attendance a
    JOIN Employees e ON a.emp_id = e.emp_id
    WHERE a.emp_id = ? AND a.date LIKE ?
    """, (emp_id, month + "%"))

    rows = cursor.fetchall()

    for r in rows:
        print("-" * 30)
        print(f"Name: {r[0]}, Date: {r[1]}, Status: {r[2]}")


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
    print("8. Sort Employees")
    print("9. Filter Employees")
    print("10. Mark Attendance")
    print("11. View Attendance")
    print("12. Attendance Report")
    print("13. Monthly Attendance")
    print("14. Exit")

    ch = input("Enter choice: ")

    if ch == "1": add_department()
    elif ch == "2": view_departments()
    elif ch == "3": add_employee()
    elif ch == "4": view_employees()
    elif ch == "5": search_employee()
    elif ch == "6": update_employee()
    elif ch == "7": delete_employee()
    elif ch == "8": sort_employees()
    elif ch == "9": filter_employees()
    elif ch == "10": mark_attendance()
    elif ch == "11": view_attendance()
    elif ch == "12": attendance_report()
    elif ch == "13": employee_monthly_attendance()
    elif ch == "14":
        break
    else:
        print("Invalid choice")

conn.close()
print("Application Closed")