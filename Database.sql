-- Create the HR database
CREATE DATABASE hr_app;

-- Connect to the database (use \c hr_app in psql)

-- Create Departments table
CREATE TABLE Departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100),
    manager_id INTEGER  -- Foreign key to Employees, added later
);

-- Create Positions table
CREATE TABLE Positions (
    position_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    salary_range_min DECIMAL(10, 2),
    salary_range_max DECIMAL(10, 2),
    department_id INTEGER REFERENCES Departments(department_id) ON DELETE CASCADE
);

-- Create Employees table
CREATE TABLE Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hire_date DATE NOT NULL,
    department_id INTEGER REFERENCES Departments(department_id) ON DELETE SET NULL,
    position_id INTEGER REFERENCES Positions(position_id) ON DELETE SET NULL
);

-- Add foreign key for manager_id in Departments (self-referencing Employees)
ALTER TABLE Departments
ADD CONSTRAINT fk_manager
FOREIGN KEY (manager_id) REFERENCES Employees(employee_id) ON DELETE SET NULL;

-- Indexes for performance
CREATE INDEX idx_employee_department ON Employees(department_id);
CREATE INDEX idx_position_department ON Positions(department_id);
