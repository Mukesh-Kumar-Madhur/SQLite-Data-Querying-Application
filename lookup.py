import sqlite3
import json
from tabulate import tabulate
import xml.etree.ElementTree as ET

# Attempt to connect to the SQLite database
try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error as e:
    print(f"Error connecting to the database: {e}")
    quit()

# Create a cursor object for executing SQL queries
cur = conn.cursor()

# Function to check if the number of arguments provided is correct
def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False

# Function to store the query result in a JSON file
def store_data_as_json(data, filename):
    try:
        with open(filename, 'w') as json_file:
            # Convert the query result to a list of dictionaries
            json_data = [dict(zip([column[0] for column in cur.description], row)) for row in data]
            json.dump(json_data, json_file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

# Function to store the query result in an XML file
def store_data_as_xml(data, filename):
    try:
        root = ET.Element("root")
        # Get the column names from the cursor description
        columns = [column[0] for column in cur.description]
        for row in data:
            item = ET.SubElement(root, "item")
            for col_name, col_value in zip(columns, row):
                child = ET.SubElement(item, col_name)
                child.text = str(col_value)
        tree = ET.ElementTree(root)
        tree.write(filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to XML: {e}")

# Function to offer the user an option to store the query result
def offer_to_store(data):
    while True:
        try:
            print("Would you like to store this result?")
            choice = input("Y/[N]? : ").strip().lower()

            if choice == "y":
                filename = input("Specify filename. Must end in .xml or .json: ")
                ext = filename.split(".")[-1]
                if ext == 'xml':
                    store_data_as_xml(data, filename)
                elif ext == 'json':
                    store_data_as_json(data, filename)
                else:
                    print("Invalid file extension. Please use .xml or .json")
            elif choice == 'n':
                break
            else:
                print("Invalid choice")
        except Exception as e:
            print(f"Error offering storage option: {e}")

# Main usage instructions
usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

# Main loop to handle user commands
while True:
    print()
    # Get input from user and split it into command and arguments
    user_input = input(usage).split(" ")
    print()

    # Parse the first word as the command
    command = user_input[0]
    # If there are additional arguments, extract them
    if len(user_input) > 1:
        args = user_input[1:]

    try:
        # Demo - Print all student names and surnames
        if command == 'd':
            data = cur.execute("SELECT first_name, last_name FROM Student").fetchall()
            for firstname, surname in data:
                print(f"{firstname} {surname}")

        # View subjects by student ID
        elif command == 'vs':
            if usage_is_incorrect(user_input, 1):
                continue
            student_id = args[0]

            # Fetch the subjects taken by the student
            data = cur.execute('''
                SELECT course_name 
                FROM Course
                JOIN StudentCourse ON Course.course_code = StudentCourse.course_code
                WHERE student_id = ?
            ''', (student_id,)).fetchall()

            # Display the result
            if data:
                print(f"Subjects taken by student {student_id}: {[row[0] for row in data]}")
            else:
                print(f"No subjects found for student {student_id}")
            offer_to_store(data)

        # Look up address by first name and surname
        elif command == 'la':
            if usage_is_incorrect(user_input, 2):
                continue
            firstname, surname = args[0], args[1]

            # Fetch the address of the student
            data = cur.execute('''
                SELECT street, city 
                FROM Address
                JOIN Student ON Student.address_id = Address.address_id
                WHERE first_name = ? AND last_name = ?
            ''', (firstname, surname)).fetchall()

            # Display the result
            if data:
                print(f"Address: {data[0][0]}, {data[0][1]}")
            else:
                print(f"No address found for {firstname} {surname}")
            offer_to_store(data)

        # List reviews by student ID
        elif command == 'lr':
            if usage_is_incorrect(user_input, 1):
                continue
            student_id = args[0]

            # Fetch the reviews of the student
            data = cur.execute('''
                SELECT completeness, efficiency, style, documentation, review_text
                FROM Review
                WHERE student_id = ?
            ''', (student_id,)).fetchall()

            # Display the result
            if data:
                for row in data:
                    print(f"Completeness: {row[0]}, Efficiency: {row[1]}, Style: {row[2]}, Documentation: {row[3]}, Review: {row[4]}")
            else:
                print(f"No reviews found for student {student_id}")
            offer_to_store(data)

        # List courses by teacher ID
        elif command == 'lc':
            if usage_is_incorrect(user_input, 1):
                continue
            teacher_id = args[0]

            # Fetch the courses taught by the teacher
            data = cur.execute('''
                SELECT course_name 
                FROM Course
                WHERE teacher_id = ?
            ''', (teacher_id,)).fetchall()

            # Display the result
            if data:
                print(f"Courses taught by teacher {teacher_id}: {[row[0] for row in data]}")
            else:
                print(f"No courses found for teacher {teacher_id}")
            offer_to_store(data)

    # List students who haven't completed their course
        elif command == 'lnc':
            # Fetch students who haven't completed their courses
            data = cur.execute('''
                SELECT Student.student_id, first_name, last_name, email, course_name
                FROM Student
                JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
                JOIN Course ON StudentCourse.course_code = Course.course_code
                WHERE is_complete = 0
            ''').fetchall()

            # Display the result
            if data:
                headers = ["Student ID", "First Name", "Last Name", "Email", "Course Name"]
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print("No students found who haven't completed their course.")
            offer_to_store(data)

        # List students who completed and got <= 30
        elif command == 'lf':
            # Fetch students who completed their course and got a mark <= 30
            data = cur.execute('''
                SELECT Student.student_id, first_name, last_name, email, course_name, mark
                FROM Student
                JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
                JOIN Course ON StudentCourse.course_code = Course.course_code
                WHERE is_complete = 1 AND mark <= 30
            ''').fetchall()

            # Display the result
            if data:
                headers = ["Student ID", "First Name", "Last Name", "Email", "Course Name", "Mark"]
                print(tabulate(data, headers=headers, tablefmt="grid"))
            else:
                print("No students found with a mark of 30 or below.")
            offer_to_store(data)

        # Exit the program
        elif command == 'e':
            print("Programme exited successfully!")
            break

        else:
            print(f"Incorrect command: '{command}'")

    except sqlite3.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
