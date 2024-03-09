import unittest
from examTopic1 import Employee, Department, Company, save_data, load_data
import os

class TestEmployeeManagementSystem(unittest.TestCase):
    def setUp(self):
        self.company = Company()

    def test_employee_creation(self):
        employee = Employee("John Doe", "001", "Manager", "HR")
        self.assertEqual(employee.name, "John Doe")
        self.assertEqual(employee.employee_id, "001")
        self.assertEqual(employee.title, "Manager")
        self.assertEqual(employee.department, "HR")

    def test_department_creation(self):
        department = Department("HR")
        self.assertEqual(department.name, "HR")
        self.assertEqual(department.employees, [])

    def test_add_employee_to_department(self):
        department = Department("HR")
        employee = Employee("John Doe", "001", "Manager", "HR")
        department.add_employee(employee)
        self.assertIn(employee, department.employees)

    def test_remove_employee_from_department(self):
        department = Department("HR")
        employee = Employee("John Doe", "001", "Manager", "HR")
        department.add_employee(employee)
        department.remove_employee(employee)
        self.assertNotIn(employee, department.employees)

    def test_add_department_to_company(self):
        department = Department("HR")
        self.company.add_department(department)
        self.assertIn("HR", self.company.departments)

    def test_remove_department_from_company(self):
        department = Department("HR")
        self.company.add_department(department)
        self.company.remove_department("HR")
        self.assertNotIn("HR", self.company.departments)

    def test_save_and_load_data(self):
        department = Department("HR")
        employee = Employee("John Doe", "001", "Manager", "HR")
        department.add_employee(employee)
        self.company.add_department(department)
        save_data(self.company)
        loaded_company = load_data()
        self.assertEqual(loaded_company.departments["HR"].employees[0].name, "John Doe")

    def tearDown(self):
        if os.path.exists("company_data.json"):
            os.remove("company_data.json")

if __name__ == "__main__":
    unittest.main()
