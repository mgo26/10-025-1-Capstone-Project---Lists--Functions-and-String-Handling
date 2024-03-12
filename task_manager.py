# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#---Variable declarations---

selected_task = None

#Functions

#Function to register a new user
def reg_user():
    new_username = input("New Username: ")
    while True:
        if new_username not in username_password.keys():
            new_password = input("New Password: ")
            confirm_password = input("Confirm Password: ")
            while True:
                #Check passwords match
                if new_password == confirm_password:
                    #If they are then add them to the user.txt file
                    print("New user added")
                    username_password[new_username] = new_password

                    with open("user.txt", "w") as out_file:
                        user_data = []
                        for k in username_password:
                            user_data.append(f"{k};{username_password[k]}")
                        out_file.write("\n".join(user_data))
                    break
                #If passwords don't match print error message and return to menu
                else:
                    print("Passwords do not match")
                    break
            break
        else:
            print("Please ensure you enter a new user")
            break

#Function to add a new task
def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    while True:
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            break
        else:
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
            ''' Add the data to the file task.txt and
                Include 'No' to indicate if the task is complete.'''
            new_task = {
                "username": task_username,
                "title": task_title,
                "description": task_description,
                "due_date": due_date_time,
                "assigned_date": curr_date,
                "completed": False
            }

            task_list.append(new_task)
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            print("Task successfully added.")
            break 

#Function to view all tasks
def view_all():  
    '''Reads the task from task.txt file and prints to the console in the 
format of Output 2 presented in the task pdf (i.e. includes spacing
and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


#Function to view my tasks
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    #Counter added to the functionality of the task, allows user to select a task to edit
    counter = 1
    temp_user_task_list = []

    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task Number: \t {str(counter)}\n"
            counter += 1
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task completed: \n {t['completed']}\n"
            print(disp_str)
            
            temp_user_task_list.append(t)
    

    #Check that the user selected a valid task
    while True:
        user_choice = int(input("Please select a task to edit or select '-1' to return to the main menu: "))
        if 1 <= user_choice <= len(temp_user_task_list):
            selected_task = temp_user_task_list[user_choice-1]

            #Asking if user wants to edit data
            task_complete = input("Is the task completed? (y/n): ")
            if task_complete == "y":
                selected_task['completed'] = True
            else:
                selected_task['completed'] = False
            
            
            #Asking if they want to edit the username
            edit_user = input("Would you like to edit the user for this task?: (y/n): ")
            if edit_user == "y":
                edited_user = input("Please enter the new user you would like to assign this task to: ")
                selected_task['username'] = edited_user
            else:
                break

            #Asking user if they want to edit the due date
            edit_due_date = input("Would you like to edit the due date for this task?: (y/n): ")
            if edit_due_date == "y":
                while True:
                    try:
                        task_due_date = input("Due date of task (YYYY-MM-DD): ")
                        due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                        selected_task['due_date'] = due_date_time
                        break

                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")
            
            else:
                break

            #write data back to list
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            print("Task successfully updated!")

        elif user_choice == -1:
            break
        else:
            print("Please make a valid selection")
            continue


#Report generator function

def generate_reports():

    #---task_overview section of function---

    #define global variables
    completed_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0

    #opens and reads file for number of tasks
    with open("tasks.txt", "r") as task_file:
        number_tasks = len(task_file.readlines())

    #iterates through tasks checking for completion
    with open("tasks.txt", "r") as task_file:
        for line in task_file:
            if "Yes" in line:
                completed_tasks += 1
            else:
                incomplete_tasks += 1

    #check for overdue tasks
    with open("tasks.txt", 'r') as task_file:
        current_date = datetime.today()
        for line in task_file:
            temp_list = line.split(";")
            due_time = datetime.strptime(temp_list[3], DATETIME_STRING_FORMAT)
            if current_date > due_time and "No" in line:
                overdue_tasks += 1

    #calculate % overdue
    with open('tasks.txt', 'r') as task_file:
        percentage_overdue = int((overdue_tasks / len(task_file.readlines()) * 100))

    #calculate % incomplete
    with open('tasks.txt', 'r') as task_file:
        percentage_incomplete = int((incomplete_tasks / len(task_file.readlines()) * 100))

  
    #write to the the task_overview file
    with open("task_overview.txt", "w") as task_overview:
        task_overview.writelines(f"The total number of tasks is: {number_tasks}\n")
        task_overview.writelines(f"The number of completed tasks is: {completed_tasks}\n")
        task_overview.writelines(f"The numer of incomplete tasks is: {incomplete_tasks}\n")
        task_overview.writelines(f"The number of tasks that are overdue is: {overdue_tasks}\n")
        task_overview.writelines(f"The percentage of tasks overdue is: {percentage_overdue}%\n")
        task_overview.writelines(f"The percentage of tasks that are incomplete is: {percentage_incomplete}%\n")


    #---user_overview section---
    
    

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()
        

    elif menu == 'va':
        view_all()
            

    elif menu == 'vm':
        view_mine()
                
    elif menu == 'gr':
        generate_reports()
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")


