import sqlite3


# Connect to SQLite. The database file is created if it does not already exist.
connection = sqlite3.connect("company.db")

# Create a cursor so that SQL statements can be executed.
cursor = connection.cursor()

# Create the tables. Dropping them first keeps the script repeatable.
cursor.execute("DROP TABLE IF EXISTS employee")
cursor.execute("DROP TABLE IF EXISTS department")

cursor.execute("""
	CREATE TABLE department (
		id INTEGER PRIMARY KEY,
		name TEXT,
		location TEXT
	)
""")

cursor.execute("""
	CREATE TABLE employee (
		id INTEGER PRIMARY KEY,
		name TEXT,
		deptid INTEGER
	)
""")

# Insert exactly five departments. The Support department has no employees.
departments = [
	(1, "Human Resources", "Mumbai"),
	(2, "Finance", "Delhi"),
	(3, "Technology", "Bengaluru"),
	(4, "Sales", "Chennai"),
	(5, "Support", "Hyderabad"),
]

# Insert exactly five employees. Employee 5 has no matching department.
employees = [
	(1, "Aarav Sharma", 1),
	(2, "Diya Patel", 2),
	(3, "Kabir Singh", 3),
	(4, "Meera Nair", 4),
	(5, "Rohan Das", 99),
]

# Execute SQL to insert the records into both tables.
cursor.executemany(
	"INSERT INTO department (id, name, location) VALUES (?, ?, ?)",
	departments,
)
cursor.executemany(
	"INSERT INTO employee (id, name, deptid) VALUES (?, ?, ?)",
	employees,
)

# Save the table changes to the database.
connection.commit()

# Fetch and display all records from the employee table.
print("Employees:")
print("ID | Name         | DeptID")
print("---|--------------|-------")
cursor.execute("SELECT id, name, deptid FROM employee")
for employee in cursor.fetchall():
	print(f"{employee[0]}  | {employee[1]:12} | {employee[2]}")

print()

# Fetch and display all records from the department table.
print("Departments:")
print("ID | Name             | Location")
print("---|------------------|---------")
cursor.execute("SELECT id, name, location FROM department")
for department in cursor.fetchall():
	print(f"{department[0]}  | {department[1]:16} | {department[2]}")

# Find and display the names of employees who work in Human Resources.
print("\nEmployees in Human Resources:")
cursor.execute("""
	SELECT employee.name
	FROM employee
	INNER JOIN department ON employee.deptid = department.id
	WHERE department.name = 'Human Resources'
""")
for employee in cursor.fetchall():
	print(employee[0])

# Close the cursor and database connection when finished.
cursor.close()
connection.close()
