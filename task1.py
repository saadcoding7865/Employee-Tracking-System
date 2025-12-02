import json
import os
import time
from datetime import datetime, date
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

DATA_FILE = "data.json"
MAX_TASKS_PER_EMP_PER_DAY = 3

# ------------ Data Persistence ------------
def load_data():
    if not os.path.exists(DATA_FILE):
        data = {
            "next_emp_id": 1,
            "next_cust_id": 1,
            "next_task_id": 1,
            "employees": {},
            "customers": {},
            "tasks": {},
            "live_locations": {}
        }
        save_data(data)
        return data

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    data.setdefault("employees", {})
    data.setdefault("customers", {})
    data.setdefault("tasks", {})
    data.setdefault("live_locations", {})
    save_data(data)
    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ------------ Helper Functions ------------
def line():
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def success(msg):
    print(Fore.GREEN + "[SUCCESS] " + msg + Style.RESET_ALL)

def error(msg):
    print(Fore.RED + "[ERROR] " + msg + Style.RESET_ALL)

def warn(msg):
    print(Fore.YELLOW + "[WARNING] " + msg + Style.RESET_ALL)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(Fore.MAGENTA + "\nPress Enter to continue..." + Style.RESET_ALL)


# ------------ ADMIN FUNCTIONS ------------
def admin_add_employees(data):
    clear()
    line()
    print(Fore.CYAN + f"{'ADD EMPLOYEES'.center(60)}")
    line()

    try:
        count = int(input("How many employees to add? : ").strip())
    except:
        error("Invalid number")
        pause()
        return

    for i in range(count):
        name = input(f"Enter employee name {i+1}: ").strip()
        if not name:
            warn("Name cannot be empty")
            continue

        eid = data["next_emp_id"]
        data["employees"][str(eid)] = {"id": eid, "name": name}
        data["next_emp_id"] += 1
        success(f"Employee Added: ID={eid}, Name={name}")

    save_data(data)
    pause()


def admin_add_customers(data):
    clear()
    line()
    print(Fore.CYAN + f"{'ADD CUSTOMERS'.center(60)}")
    line()

    try:
        count = int(input("How many customers to add? : ").strip())
    except:
        error("Invalid number")
        pause()
        return

    for i in range(count):
        name = input(f"Enter customer name {i+1}: ").strip()
        if not name:
            warn("Name required")
            continue

        area = input("Enter customer area (e.g. Camp, Kothrud): ").strip()
        if not area:
            warn("Area required")
            continue

        cid = data["next_cust_id"]
        data["customers"][str(cid)] = {"id": cid, "name": name, "area": area}
        data["next_cust_id"] += 1
        success(f"Customer Added: ID={cid}, Name={name}, Area={area}")

    save_data(data)
    pause()


def admin_assign_task(data):
    clear()
    line()
    print(Fore.CYAN + f"{'ASSIGN TASK'.center(60)}")
    line()

    if not data["employees"]:
        warn("No employees available")
        pause()
        return

    if not data["customers"]:
        warn("No customers available")
        pause()
        return

    print("\nEMPLOYEES:")
    for k, v in data["employees"].items():
        print(f"  {k}) {v['name']}")

    emp_id = input("\nAssign to employee ID: ").strip()
    if emp_id not in data["employees"]:
        error("Invalid employee ID")
        pause()
        return

    print("\nCUSTOMERS:")
    for k, v in data["customers"].items():
        print(f"  {k}) {v['name']} ({v['area']})")

    cust_id = input("\nCustomer ID: ").strip()
    if cust_id not in data["customers"]:
        error("Invalid customer ID")
        pause()
        return

    task_name = input("\nEnter Task Title: ").strip()
    if not task_name:
        error("Task title required")
        pause()
        return

    sched = input("Enter schedule date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not sched:
        sched = date.today().isoformat()

    assigned_today = sum(1 for t in data["tasks"].values()
                         if str(t["employee_id"]) == emp_id and t["scheduled"] == sched)

    if assigned_today >= MAX_TASKS_PER_EMP_PER_DAY:
        warn("This employee already has 3 tasks for this day")
        pause()
        return

    customer = data["customers"][cust_id]
    tid = data["next_task_id"]

    data["tasks"][str(tid)] = {
        "id": tid,
        "task_name": task_name,
        "employee_id": int(emp_id),
        "customer_id": int(cust_id),
        "customer_name": customer["name"],
        "customer_area": customer["area"],
        "scheduled": sched,
        "status": "assigned",
        "location_verified": False,
        "location_updates": [],
        "completed_at": None,
        "review": None
    }

    data["next_task_id"] += 1
    save_data(data)
    success(f"Task Assigned Successfully! Task ID = {tid}")
    pause()


def admin_view_tasks(data):
    clear()
    line()
    print(Fore.CYAN + f"{'VIEW ALL TASKS'.center(60)}")
    line()

    if not data["tasks"]:
        warn("No tasks found")
        pause()
        return

    rows = []
    for t in data["tasks"].values():
        emp = data["employees"][str(t["employee_id"])]["name"]
        rows.append([
            t["id"],
            t["task_name"],
            emp,
            t["customer_name"],
            t["customer_area"],
            t["status"],
            "YES" if t["location_verified"] else "NO",
            t["completed_at"],
            t["review"] if t["review"] else "No Review"
        ])

    print(tabulate(rows,
                   headers=["TaskID", "Task", "Employee", "Customer", "Area", "Status",
                            "Verified", "Completed", "Review"],
                   tablefmt="grid"))
    pause()


def admin_view_locations(data):
    clear()
    line()
    print(Fore.CYAN + f"{'LIVE EMPLOYEE LOCATIONS'.center(60)}")
    line()

    rows = []
    for k, v in data["employees"].items():
        loc = data["live_locations"].get(k, {"area": "Not Updated", "time": "-"})
        rows.append([k, v["name"], loc["area"], loc["time"]])

    print(tabulate(rows, headers=["ID", "Employee", "Area", "Time"], tablefmt="grid"))
    pause()


def admin_menu(data):
    while True:
        clear()
        line()
        print(Fore.CYAN + f"{'ADMIN MENU'.center(60)}")
        line()
        print("""
[1] Add Employee
[2] Add Customer
[3] Assign Task
[4] View All Tasks
[5] View Employee Location
[0] Logout
""")
        ch = input("Enter choice: ").strip()

        if ch == "1": admin_add_employees(data)
        elif ch == "2": admin_add_customers(data)
        elif ch == "3": admin_assign_task(data)
        elif ch == "4": admin_view_tasks(data)
        elif ch == "5": admin_view_locations(data)
        elif ch == "0": break
        else:
            error("Invalid choice")
            pause()


# ------------ EMPLOYEE FUNCTIONS ------------
def employee_select(data):
    clear()
    line()
    print(Fore.CYAN + f"{'EMPLOYEE LOGIN'.center(60)}")
    line()

    if not data["employees"]:
        warn("No employees available")
        pause()
        return None

    print("\nEmployees:")
    for k, v in data["employees"].items():
        print(f"  {k}) {v['name']}")

    emp_id = input("\nEnter Employee ID: ").strip()
    if emp_id not in data["employees"]:
        error("Invalid ID")
        pause()
        return None

    return emp_id


def employee_view_tasks(data, emp_id):
    clear()
    line()
    print(Fore.CYAN + f"{'MY TASKS'.center(60)}")
    line()

    tasks = [t for t in data["tasks"].values() if str(t["employee_id"]) == emp_id]
    if not tasks:
        warn("No tasks assigned")
        pause()
        return

    rows = []
    for t in tasks:
        rows.append([t["id"], t["task_name"], t["customer_name"], t["customer_area"],
                     t["status"], "YES" if t["location_verified"] else "NO"])

    print(tabulate(rows,
                   headers=["TaskID", "Task", "Customer", "Area", "Status", "Verified"],
                   tablefmt="grid"))
    pause()


def update_location(data, emp_id, task=None):
    area = input("Enter CURRENT Area: ").strip()
    t = now()

    data["live_locations"][str(emp_id)] = {"area": area, "time": t}

    if task:
        task["location_updates"].append({"area": area, "time": t})

    save_data(data)
    success(f"Location updated to {area}")
    return area


def employee_start_task(data, emp_id):
    clear()
    line()
    print(Fore.CYAN + f"{'START TASK'.center(60)}")
    line()

    tasks = [t for t in data["tasks"].values() if str(t["employee_id"]) == emp_id]
    if not tasks:
        warn("No tasks available")
        pause()
        return

    employee_view_tasks(data, emp_id)
    clear()
    line()
    print(Fore.CYAN + f"{'START TASK'.center(60)}")
    line()

    tid = input("Enter Task ID to start: ").strip()
    task = data["tasks"].get(tid)

    if not task:
        error("Invalid Task ID")
        pause()
        return

    task["status"] = "in_progress"
    save_data(data)

    customer_area = task["customer_area"].lower()
    print(Fore.YELLOW + "\nUpdating location every 5 seconds (3 updates required)...\n")

    last_area = ""
    for i in range(3):
        last_area = update_location(data, emp_id, task)
        if i < 2:
            time.sleep(5)

    if last_area.lower() == customer_area:
        task["location_verified"] = True
        save_data(data)
        success("LOCATION VERIFIED — now you can complete the task")
    else:
        task["location_verified"] = False
        save_data(data)
        error("LOCATION NOT VERIFIED — try again closer to customer location")

    pause()


def employee_complete_task(data, emp_id):
    clear()
    line()
    print(Fore.CYAN + f"{'COMPLETE TASK'.center(60)}")
    line()

    tasks = [t for t in data["tasks"].values() if str(t["employee_id"]) == emp_id]
    if not tasks:
        warn("No tasks")
        pause()
        return

    employee_view_tasks(data, emp_id)
    clear()
    line()
    print(Fore.CYAN + f"{'COMPLETE TASK'.center(60)}")
    line()

    tid = input("Enter Task ID to complete: ").strip()
    task = data["tasks"].get(tid)

    if not task:
        error("Task not found")
        pause()
        return

    if not task["location_verified"]:
        error("Cannot complete task — Location Not Verified yet")
        pause()
        return

    task["status"] = "completed"
    task["completed_at"] = now()
    save_data(data)
    success("Task Completed Successfully!")

    pause()


def employee_menu(data):
    emp_id = employee_select(data)
    if not emp_id:
        return

    emp_name = data["employees"][emp_id]["name"]

    while True:
        clear()
        line()
        print(Fore.CYAN + f"{f'EMPLOYEE MENU - {emp_name}'.center(60)}")
        line()

        print("""
[1] View My Tasks
[2] Start Task (Live Location)
[3] Complete Task
[0] Logout
""")
        ch = input("Enter choice: ").strip()

        if ch == "1": employee_view_tasks(data, emp_id)
        elif ch == "2": employee_start_task(data, emp_id)
        elif ch == "3": employee_complete_task(data, emp_id)
        elif ch == "0": break
        else:
            error("Invalid choice")
            pause()


# ------------ CUSTOMER PANEL ------------
def customer_menu(data):
    clear()
    line()
    print(Fore.CYAN + f"{'CUSTOMER LOGIN'.center(60)}")
    line()

    if not data["customers"]:
        warn("No customers found")
        pause()
        return

    print("\nCustomers:")
    for k, v in data["customers"].items():
        print(f"  {k}) {v['name']} ({v['area']})")

    cid = input("\nEnter Customer ID: ").strip()
    if cid not in data["customers"]:
        error("Invalid ID")
        pause()
        return

    cust_name = data["customers"][cid]["name"]

    while True:
        clear()
        line()
        print(Fore.CYAN + f"{f'CUSTOMER MENU - {cust_name}'.center(60)}")
        line()

        print("""
[1] View Visits
[2] Submit Review
[0] Logout
""")

        ch = input("Enter choice: ").strip()

        if ch == "1":
            visits = [t for t in data["tasks"].values() if str(t["customer_id"]) == cid]

            if not visits:
                warn("No visits found")
                pause()
                continue

            rows = []
            for t in visits:
                emp = data["employees"][str(t["employee_id"])]["name"]
                rows.append([t["id"], t["task_name"], emp, t["status"], t["completed_at"]])

            print(tabulate(rows,
                           headers=["TaskID", "Task", "Employee", "Status", "Completed"],
                           tablefmt="grid"))
            pause()

        elif ch == "2":
            tid = input("Enter Task ID: ").strip()
            task = data["tasks"].get(tid)

            if not task:
                error("Task not found")
                pause()
                continue

            if task["status"] != "completed":
                error("Review is allowed only AFTER task is completed")
                pause()
                continue

            review = input("Enter your review: ").strip()
            if not review:
                warn("Review cannot be empty")
                pause()
                continue

            task["review"] = review
            save_data(data)
            success("Review Saved Successfully!")
            pause()

        elif ch == "0":
            break

        else:
            error("Invalid choice")
            pause()


# ------------ MAIN APP ------------
def main():
    data = load_data()
    while True:
        clear()
        line()
        print(Fore.CYAN + f"{'EMPLOYEE TRACKING SYSTEM'.center(60)}")
        line()

        print("""
[1] Admin Login
[2] Employee Login
[3] Customer Login
[0] Exit
""")

        ch = input("Enter choice: ").strip()

        if ch == "1": admin_menu(data)
        elif ch == "2": employee_menu(data)
        elif ch == "3": customer_menu(data)
        elif ch == "0":
            print(Fore.CYAN + "Goodbye!")
            break
        else:
            error("Invalid choice")
            pause()


if __name__ == "__main__":
    main()
