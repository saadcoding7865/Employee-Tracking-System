EMPLOYEE TRACKING SYSTEM

This is a Python-based console application that allows an Admin to assign tasks to employees, track their live location updates, verify task completion, and enable customers to provide feedback only after successful task completion. It simulates real-life field executive tracking without needing GPS APIs.

PROJECT FEATURES

Admin Panel:
Add multiple employees
Add multiple customers
Assign tasks with task title, allocated employee, customer and scheduled date
View all tasks in a structured table
View live employee location updates

Employee Panel:

View tasks assigned by admin

Start a task and provide live location updates three times

Task is marked verified only when location matches customer area

Complete task only after verification

Customer Panel:

View visit history

Submit review only after task is marked completed

Data Storage

The application stores all data inside a JSON file named data.json. This includes employee list, customer list, tasks, location logs, and reviews.

TECHNOLOGIES USED

Python Programming Language

JSON for data storage (file-based database)

OS module for clearing terminal screen

Time module for delay-based simulation of location updates

Datetime module for timestamps and scheduling

Colorama library for colored and styled terminal output

Tabulate library for formatted table display

HOW THE SYSTEM WORKS

Step 1: Admin logs in and adds employees and customers

Step 2: Admin assigns a task to an employee

Step 3: Employee logs in and views tasks

Step 4: Employee starts task and updates live location three times (every 5 seconds)

Step 5: If location matches customer area, location is marked verified

Step 6: Employee completes task

Step 7: Customer submits review only after task completion

Step 8: Admin can view reviews in task listing

WHY THIS PROJECT

This project is useful for organizations that need to track field sales executives or service engineers to ensure authentic on-site visits and performance monitoring.

INSTALLATION

Install required libraries:

pip install colorama tabulate

Run the script:

python task1.py

FUTURE ENHANCEMENTS

Integration with OpenStreetMap for real map location tracking

Authentication with username and password

Real-time tracking visualization for admin

Export task reports to Excel or PDF

CONCLUSION

This project demonstrates real-time tracking workflow, task management, live updates, and review validation system using Python console interface.
