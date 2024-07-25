from datetime import datetime

# Function to check if username exists in user_information dictionary


def users_info(username):
    return username in user_information

# Function to display the menu options


def display_menu(is_admin):
    if is_admin:
        print('''Select one of the following options:
        a - Add task
        r - Register new user
        va - View all tasks
        vm - View my tasks
        s - View statistics
        e - Exit
        ''')
    else:
        print('''Select one of the following options:
        a - Add task
        vm - View my tasks
        e - Exit
        ''')

# Function to count total number of users


def count_users():
    return len(user_information)

# Function to count total number of tasks


def count_tasks():
    try:
        with open('tasks.txt', 'r') as file:
            tasks = file.readlines()
            return len(tasks)
    except FileNotFoundError:
        return 0

# Function to validate date format


def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format, please enter date in YYYY-MM-DD format.")
        return None

# Function to validate completion status


def validate_completion_status(status):
    while status.lower() not in ['yes', 'no']:
        status = input("Invalid input. Please enter 'Yes' or 'No': ")
    return status.lower() == 'yes'


# Dictionary to store user information
user_information = {}

# Try to read user info from user.txt and store it in user_information dictionary
try:
    with open('user.txt', 'r') as file:
        for line in file:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) == 2:
                    username, password = parts
                    user_information[username] = password.strip()
except FileNotFoundError:
    print("User file not found. Make sure 'user.txt' exists.")

# Login loop
while True:
    username = input("Please enter username: ")
    password = input("Please enter a password: ")

    if users_info(username) and user_information[username] == password:
        print("Your login was successful.")
        is_admin = username == "admin"
        while True:
            display_menu(is_admin)
            menu = input("Enter your choice: ").lower()

            if menu == 'a':
                # Add task option
                task_username = input(
                    "Enter the username of the person to whom the task is assigned: ")
                task_name = input("Enter the task name: ")
                task_description = input("Enter task description: ")
                # Assign current date as start date
                start_date = datetime.now().strftime('%Y-%m-%d')
                end_date = validate_date(
                    input("Enter the end date (YYYY-MM-DD): "))
                if end_date is None:
                    continue
                completed = validate_completion_status(
                    input("Is the task completed? (Yes/No): "))

                with open('tasks.txt', 'a') as file:
                    file.write(f"{task_username}, {task_name}, {task_description}, {start_date}, {end_date}, {completed}\n")
                print("New task added")

            elif menu == 'r' and is_admin:
                # Register new user option (only available for admin)
                new_user = input("Enter new username: ")
                new_password = input("Enter new password: ")
                confirm_password = input("Confirm your password: ")

                if new_password == confirm_password:
                    with open('user.txt', 'a') as file:
                        file.write(f"{new_user},{new_password}\n")
                    print("User registered successfully!")
                    user_information[new_user] = new_password
                else:
                    print("Error: Passwords do not match")

            elif menu == 'va' and is_admin:
                # View all tasks option
                try:
                    with open('tasks.txt', 'r') as file:
                        tasks = file.readlines()
                        if tasks:
                            print("Tasks:")
                            for task in tasks:
                                task_details = task.strip().split(", ")
                                task_name = task_details[1]
                                task_description = task_details[2]
                                start_date = task_details[3]
                                end_date = task_details[4]
                                completed = task_details[5]

                                print("Task name:", task_name)
                                print("Task description:", task_description)
                                print("Start date:", start_date)
                                print("End date:", end_date)
                                print("Completed:", completed)
                                print()
                        else:
                            print("No tasks found.")
                except FileNotFoundError:
                    print("Task file not found. Make sure 'tasks.txt' exists.")

            elif menu == 'vm':
                # View my tasks option
                found_tasks = False
                try:
                    with open('tasks.txt', 'r') as file:
                        tasks = file.readlines()
                        for task in tasks:
                            assigned_to = task.split(",")[0].strip()
                            if username == assigned_to:
                                task_details = task.strip().split(", ")
                                task_name = task_details[1]
                                task_description = task_details[2]
                                start_date = task_details[3]
                                end_date = task_details[4]
                                completed = task_details[5]

                                print("Task name:", task_name)
                                print("Task description:", task_description)
                                print("Start date:", start_date)
                                print("End date:", end_date)
                                print("Completed:", completed)
                                print()
                                found_tasks = True
                except FileNotFoundError:
                    print("Task file not found. Make sure 'tasks.txt' exists.")

                if not found_tasks:
                    print("No tasks found for the given username.")

            elif menu == 's' and is_admin:
                # View statistics option (only available for admin)
                print("Statistics:")
                print("Total users:", count_users())
                print("Total tasks:", count_tasks())

            elif menu == 'e':
                # Exit option
                print('Goodbye!')
                break

            else:
                print("You have entered an invalid input. Please try again.")

        break

    else:
        print("Login error. Please check username and password")

file.close()
