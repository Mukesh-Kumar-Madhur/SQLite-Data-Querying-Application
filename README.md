### Title: **SQLite Data Querying Application**

---

### Description:

This project is a Python-based application designed to query a SQLite database and present the data to the user in various formats (tabular, JSON, XML). The user can perform several predefined queries, store the results in files, and interact with the data through the command-line interface. The database structure includes information about students, courses, reviews, and addresses.

---

### Repository Structure:

- `HyperionDev.db` (SQLite database)
- `query_app.py` (Main Python script)
- `README.md` (Instructions on how to use the application)
- `.gitignore` (Optional but recommended to ignore unnecessary files)

---

### README.md

```markdown
# SQLite Data Querying Application

## Project Description
This application allows users to interact with an SQLite database, query various types of data, and store query results in different formats. The app includes functionality to:
- Query student data, courses, and reviews.
- View or store data in either JSON or XML format.
- Tabulate the results for better readability.
  
## Features
1. **Query student subjects by ID**.
2. **Look up a student's address by first and last name**.
3. **List reviews for a specific student**.
4. **List courses taught by a specific teacher**.
5. **List students who haven’t completed their courses**.
6. **List students who completed their course but scored <= 30**.
7. **Store query results in JSON or XML format**.

## Prerequisites
- Python 3.x installed on your machine.
- Required Python libraries:
  - `sqlite3` (standard library)
  - `json` (standard library)
  - `tabulate` (`pip install tabulate`)
  - `xml.etree.ElementTree` (standard library)

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sqlite-query-app.git
cd sqlite-query-app
```

### 2. Install Dependencies
```bash
pip install tabulate
```

### 3. Add Database
Ensure that `HyperionDev.db` is present in the same directory as `query_app.py`.

### 4. Run the Application
```bash
python query_app.py
```

## Application Usage

Once we run the app, we will be prompted with a menu. Enter the corresponding command to execute a specific query:

```text
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program
```

### Commands:

- **d**: Demo mode – displays all students’ first and last names.
- **vs <student_id>**: View the subjects taken by a student.
- **la <firstname> <surname>**: Look up the address for a given first name and surname.
- **lr <student_id>**: List reviews for a student by their ID.
- **lc <teacher_id>**: List courses taken by a teacher by their ID.
- **lnc**: List all students who haven't completed their course.
- **lf**: List students who completed their course and scored <= 30.
- **e**: Exit the application.

### Example Commands:
- To view subjects taken by a student with ID `123`:
```bash
vs 123
```
- To list all courses taught by a teacher with ID `45`:
```bash
lc 45
```

### Storing Results:
The app will ask if you want to store the query result in a file after each query. If you choose to store the result, provide a filename ending in `.json` or `.xml`.

### JSON Example:
```json
[
    {
        "student_id": 123,
        "first_name": "John",
        "last_name": "Doe",
        "course_name": "Mathematics"
    }
]
```

### XML Example:
```xml
<root>
    <item>
        <student_id>123</student_id>
        <first_name>John</first_name>
        <last_name>Doe</last_name>
        <course_name>Mathematics</course_name>
    </item>
</root>
```

## Error Handling
- The app will notify users if there’s an error in the database connection or if incorrect commands/arguments are provided.
- Prompts are clear and user-friendly to guide through invalid entries.

