import os
from datetime import datetime, date

# Define the datetime format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to register a new user
def reg_user(username_password):
    """
    Register a new user with a username and password.
    """
    new_username = input("New Username: ")

    if new_username in username_password.keys():
        print("Username already exists.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task(task_list, username_password):
    """
    Add a new task to the task list.
    """
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"\n{task_username};{task_title};{task_description};{due_date_time.strftime(DATETIME_STRING_FORMAT)};{curr_date.strftime(DATETIME_STRING_FORMAT)};No")
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    """
    View all tasks stored in the task list.
    """
    for index, t in enumerate(task_list, start=1):
        disp_str = f"Task {index}:\n"
        disp_str += f"Title: {t['title']}\n"
        disp_str += f"Assigned to: {t['username']}\n"
        disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Description: {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(task_list, curr_user):
    """
    View tasks assigned to the current user.
    """
    print("Your tasks:")
    for index, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            disp_str = f"Task {index}:\n"
            disp_str += f"Title: {t['title']}\n"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Description: {t['description']}\n"
            print(disp_str)

# Function to mark a task as complete
def mark_complete(task_list, task_index):
    """
    Mark a task as complete.
    """
    task_list[task_index]['completed'] = True
    with open("tasks.txt", "w") as task_file:
        for t in task_list:
            task_file.write(f"{t['username']};{t['title']};{t['description']};{t['due_date'].strftime(DATETIME_STRING_FORMAT)};{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if t['completed'] else 'No'}\n")
    print("Task marked as complete.")

# Function to edit a task
def edit_task(task_list, task_index):
    """
    Edit a task's username or due date.
    """
    print("Edit Task")
    field_to_edit = input("Enter 'username' or 'due_date': ").lower()
    if field_to_edit == 'username':
        new_username = input("Enter new username: ")
        task_list[task_index]['username'] = new_username
    elif field_to_edit == 'due_date':
        while True:
            try:
                new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                task_list[task_index]['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")
    else:
        print("Invalid field to edit.")
        return

    with open("tasks.txt", "w") as task_file:
        for t in task_list:
            task_file.write(f"{t['username']};{t['title']};{t['description']};{t['due_date'].strftime(DATETIME_STRING_FORMAT)};{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if t['completed'] else 'No'}\n")
    print("Task edited successfully.")

# Function to display statistics
def display_statistics():
    """
    Display statistics from the generated report text files.
    """
    try:
        with open("task_overview.txt", "r") as task_file:
            print(task_file.read())
        with open("user_overview.txt", "r") as user_file:
            print(user_file.read())
    except FileNotFoundError:
        print("Reports have not been generated yet.")

# Check if tasks.txt exists, if not create it
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w"):
        pass

# Read tasks from tasks.txt and convert to dictionary
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}
    task_components = t_str.split(";")
    if len(task_components) == 6:
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

# Check if user.txt exists, if not create it with default admin account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read usernames and passwords from user.txt
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

username_password = {}
for user in user_data:
    user_info = user.split(';')
    if len(user_info) == 2:
        username, password = user_info
        username_password[username] = password

# User Login
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user in username_password and username_password[curr_user] == curr_pass:
        print("Login Successful!")
        logged_in = True
    else:
        print("Invalid credentials")

# Main Menu
while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)
    elif menu == 'a':
        add_task(task_list, username_password)
    elif menu == 'va':
        view_all(task_list)
    elif menu == 'vm':
        view_mine(task_list, curr_user)
        task_index = int(input("Enter the number of the task you want to edit: "))
        if task_index >= 1 and task_index <= len(task_list):
            edit_choice = input("Enter 'c' to mark as complete or 'e' to edit the task: ").lower()
            if edit_choice == 'c':
                mark_complete(task_list, task_index - 1)
            elif edit_choice == 'e':
                edit_task(task_list, task_index - 1)
            else:
                print("Invalid choice.")
    elif menu == 'ds' and curr_user == 'admin':
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")
