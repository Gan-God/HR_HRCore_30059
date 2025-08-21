import streamlit as st
import pandas as pd
from psycopg2 import sql
import db_utils

# Streamlit App
st.title("HRCore: HR Management System")

# Simulate role-based access control
role = st.selectbox("Select User Role", ["Admin", "HR Manager", "Employee"])
st.write(f"Logged in as: {role}")

# Tabs for different entities
tab1, tab2, tab3 = st.tabs(["Employees", "Departments", "Positions"])

# Employees Tab
with tab1:
    st.subheader("Manage Employees")
    
    # Read: Display Employees
    if role in ["Admin", "HR Manager"]:
        query = "SELECT e.employee_id, e.first_name, e.last_name, e.email, e.hire_date, d.name AS department, p.title AS position FROM Employees e LEFT JOIN Departments d ON e.department_id = d.department_id LEFT JOIN Positions p ON e.position_id = p.position_id"
    else:  # Employee role: only self-data (simulated, assumes employee_id=1)
        query = "SELECT e.employee_id, e.first_name, e.last_name, e.email, e.hire_date, d.name AS department, p.title AS position FROM Employees e LEFT JOIN Departments d ON e.department_id = d.department_id LEFT JOIN Positions p ON e.position_id = p.position_id WHERE e.employee_id = 1"
    
    employees_df, error = db_utils.fetch_data(query)
    if error:
        st.error(error)
    else:
        st.dataframe(employees_df)

    # Create Employee (Admin/HR Manager only)
    if role in ["Admin", "HR Manager"]:
        with st.form("create_employee"):
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            hire_date = st.date_input("Hire Date")
            dept_name = st.text_input("Department Name")
            pos_title = st.text_input("Position Title")
            submit = st.form_submit_button("Add Employee")
            
            if submit:
                query = sql.SQL("""
                    INSERT INTO Employees (first_name, last_name, email, hire_date, department_id, position_id)
                    VALUES (%s, %s, %s, %s, (SELECT department_id FROM Departments WHERE name = %s), 
                           (SELECT position_id FROM Positions WHERE title = %s))
                """)
                success, error = db_utils.execute_query(query, (first_name, last_name, email, hire_date, dept_name, pos_title))
                if success:
                    st.success("Employee added successfully!")
                else:
                    st.error(error or "Failed to add employee. Ensure department and position exist.")

    # Update Employee (Admin/HR Manager or Employee for personal info)
    if role in ["Admin", "HR Manager", "Employee"]:
        with st.form("update_employee"):
            emp_id = st.number_input("Employee ID to Update", min_value=1, step=1)
            new_email = st.text_input("New Email (leave blank to keep unchanged)")
            submit = st.form_submit_button("Update Email")
            
            if submit and new_email:
                query = sql.SQL("UPDATE Employees SET email = %s WHERE employee_id = %s")
                success, error = db_utils.execute_query(query, (new_email, emp_id))
                if success:
                    st.success("Employee updated successfully!")
                else:
                    st.error(error or "Update failed. Check employee ID.")

    # Delete Employee (Admin/HR Manager only)
    if role in ["Admin", "HR Manager"]:
        with st.form("delete_employee"):
            emp_id = st.number_input("Employee ID to Delete", min_value=1, step=1)
            submit = st.form_submit_button("Delete Employee")
            
            if submit:
                query = sql.SQL("DELETE FROM Employees WHERE employee_id = %s")
                success, error = db_utils.execute_query(query, (emp_id,))
                if success:
                    st.success("Employee deleted successfully!")
                else:
                    st.error(error or "Delete failed. Check employee ID.")

# Departments Tab
with tab2:
    st.subheader("Manage Departments")
    
    # Read: Display Departments
    if role in ["Admin", "HR Manager"]:
        query = "SELECT d.department_id, d.name, d.location, e.first_name || ' ' || e.last_name AS manager FROM Departments d LEFT JOIN Employees e ON d.manager_id = e.employee_id"
    else:
        query = "SELECT d.department_id, d.name, d.location FROM Departments d JOIN Employees e ON d.department_id = e.department_id WHERE e.employee_id = 1"
    
    depts_df, error = db_utils.fetch_data(query)
    if error:
        st.error(error)
    else:
        st.dataframe(depts_df)

    # Create Department (Admin/HR Manager only)
    if role in ["Admin", "HR Manager"]:
        with st.form("create_department"):
            dept_name = st.text_input("Department Name")
            location = st.text_input("Location")
            submit = st.form_submit_button("Add Department")
            
            if submit:
                query = sql.SQL("INSERT INTO Departments (name, location) VALUES (%s, %s)")
                success, error = db_utils.execute_query(query, (dept_name, location))
                if success:
                    st.success("Department added successfully!")
                else:
                    st.error(error or "Failed to add department.")

# Positions Tab
with tab3:
    st.subheader("Manage Positions")
    
    # Read: Display Positions
    if role in ["Admin", "HR Manager"]:
        query = "SELECT p.position_id, p.title, p.salary_range_min, p.salary_range_max, d.name AS department FROM Positions p LEFT JOIN Departments d ON p.department_id = d.department_id"
    else:
        query = "SELECT p.position_id, p.title, p.salary_range_min, p.salary_range_max, d.name AS department FROM Positions p JOIN Employees e ON p.position_id = e.position_id LEFT JOIN Departments d ON p.department_id = d.department_id WHERE e.employee_id = 1"
    
    positions_df, error = db_utils.fetch_data(query)
    if error:
        st.error(error)
    else:
        st.dataframe(positions_df)

    # Create Position (Admin/HR Manager only)
    if role in ["Admin", "HR Manager"]:
        with st.form("create_position"):
            title = st.text_input("Position Title")
            salary_min = st.number_input("Salary Range Min", min_value=0.0, step=1000.0)
            salary_max = st.number_input("Salary Range Max", min_value=0.0, step=1000.0)
            dept_name = st.text_input("Department Name")
            submit = st.form_submit_button("Add Position")
            
            if submit:
                query = sql.SQL("""
                    INSERT INTO Positions (title, salary_range_min, salary_range_max, department_id)
                    VALUES (%s, %s, %s, (SELECT department_id FROM Departments WHERE name = %s))
                """)
                success, error = db_utils.execute_query(query, (title, salary_min, salary_max, dept_name))
                if success:
                    st.success("Position added successfully!")
                else:
                    st.error(error or "Failed to add position. Ensure department exists.")

# Footer
st.write("HRCore: Powered by Streamlit, PostgreSQL, Pandas, and Psycopg2")