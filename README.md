# Employee Management System

This project is an Employee Management System built using Flask and MySQL. It provides functionalities for managing employee records and includes an admin login feature.

## Project Structure

```
employee-management-system
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates
│   │   ├── base.html
│   │   ├── login.html
│   │   └── dashboard.html
│   └── static
│       ├── css
│       │   └── styles.css
│       └── js
│           └── scripts.js
├── migrations
│   └── README.md
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Features

- Admin login functionality
- Employee management (add, update, delete)
- Dashboard for admin to view employee records

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd employee-management-system
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='mysql+pymysql://root:@localhost/employee_management?charset=utf8mb4'
   ```

5. Set up the MySQL database:
   - Create a database named `employee_management`.
   - Run the SQL file to create tables and insert the admin user.

6. Run the application:
   ```
   python run.py
   ```

## Usage

- Access the application at `http://127.0.0.1:5000/`.
- Use the admin credentials to log in.

## SQL File

An SQL file is provided to create the necessary tables and insert an admin user with a predefined password. Please ensure to change the password after the initial setup for security reasons.