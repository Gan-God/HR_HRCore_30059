# HR_HRCore_30059
HRCore is a domain-specific CRUD application designed for human resource management, enabling efficient employee, department, and position data handling. It provides role-based access control (RBAC) for three user types—Admin, HR Manager, and Employee—with tailored Create, Read, Update, and Delete (CRUD) operations. Key functions include:

Employee Management: Admins and HR Managers can create (hire), read (view profiles), update (edit details or reassign), and delete (terminate) employee records. Employees can view and update their personal information.
Department Management: Admins can create, update, or delete departments, while HR Managers can assign managers and view details. Employees can view their own department's information.
Position Management: Admins and HR Managers can define and update job positions, including salary ranges, while employees can view their assigned position.
Data Integrity: Built on PostgreSQL, HRCore ensures ACID-compliant transactions for reliable operations, such as atomic employee hires or department updates, preventing data inconsistencies.
Security: Implements RBAC to restrict operations based on user roles, ensuring data privacy and compliance.

HRCore streamlines HR processes with a secure, scalable database and intuitive CRUD functionality, suitable for organizations of varying sizes.
