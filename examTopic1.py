import json

class Employee:
    def __init__(self, name, employee_id, title, department):
        self.name = name
        self.employee_id = employee_id
        self.title = title
        self.department = department

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"ID: {self.employee_id}")
        print(f"Title: {self.title}")
        print(f"Department: {self.department}")

    def __str__(self):
        return f"{self.name} - {self.employee_id}"

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        self.employees.remove(employee)

    def list_employees(self):
        for employee in self.employees:
            print(employee)

class Company:
    def __init__(self):
        self.departments = {}

    def add_department(self, department):
        self.departments[department.name] = department

    def remove_department(self, department_name):
        del self.departments[department_name]

    def display_departments(self):
        for department_name, department in self.departments.items():
            print(f"Department: {department_name}")
            department.list_employees()
            print()

def save_data(company):
    data = {
        "departments": {}
    }
    for department_name, department in company.departments.items():
        data["departments"][department_name] = [str(employee) for employee in department.employees]

    with open("company_data.json", "w") as file:
        json.dump(data, file)

def load_data():
    try:
        with open("company_data.json", "r") as file:
            data = json.load(file)
            company = Company()
            for department_name, employees in data["departments"].items():
                department = Department(department_name)
                for employee_str in employees:
                    name, employee_id = employee_str.split(" - ")
                    employee = Employee(name, employee_id, "", department_name)
                    department.add_employee(employee)
                company.add_department(department)
            return company
    except FileNotFoundError:
        return Company()

def print_menu():
    print("Employee Management System Menu:")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. List Employees in Department")
    print("4. Add Department")
    print("5. Remove Department")
    print("6. List Departments")
    print("7. Save and Quit")

def main():
    company = load_data()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter employee name: ")
            employee_id = input("Enter employee ID: ")
            department_name = input("Enter department name: ")

            if department_name in company.departments:
                title = input("Enter employee title: ")
                employee = Employee(name, employee_id, title, department_name)
                department = company.departments[department_name]
                department.add_employee(employee)
            else:
                print("Department not found.")

        elif choice == "2":
            department_name = input("Enter department name: ")

            if department_name in company.departments:
                department = company.departments[department_name]
                print("Employees in department:")
                department.list_employees()
                employee_id = input("Enter employee ID to remove: ")

                for employee in department.employees:
                    if employee.employee_id == employee_id:
                        department.remove_employee(employee)
                        print("Employee removed.")
                        break
                else:
                    print("Employee ID not found.")
            else:
                print("Department not found.")

        elif choice == "3":
            department_name = input("Enter department name: ")

            if department_name in company.departments:
                department = company.departments[department_name]
                print(f"Employees in {department_name} department:")
                department.list_employees()
            else:
                print("Department not found.")

        elif choice == "4":
            department_name = input("Enter department name: ")
            department = Department(department_name)
            company.add_department(department)
            print("Department added.")

        elif choice == "5":
            department_name = input("Enter department name to remove: ")
            if department_name in company.departments:
                company.remove_department(department_name)
                print("Department removed.")
            else:
                print("Department not found.")

        elif choice == "6":
            print("List of departments:")
            company.display_departments()

        elif choice == "7":
            save_data(company)
            print("Data saved. Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
