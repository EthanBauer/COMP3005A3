# IMport psycopg packages
import psycopg
from psycopg import errors

# connection function
def connect():
    try:
        # connection parameters
        conn = psycopg.connect(
            dbname="Assignment3",
            user="postgres",
            password="Hannah14!",
            host="localhost",
            port="5432"
        )
        return conn
    # on error, print the error for debugging.
    except errors.Error as e:
        print(f"Error: Unable to connect to the database: {e}")
        return None

# function for closing database
def close_connection(conn):
    try:
        # close the connection
        conn.close()
        print("Connection closed.")
    # again, print error for debugging
    except errors.Error as e:
        print(f"Error: Unable to close connection: {e}")

# function for printing all students in database
def getAllStudents():
    # establish connection string
    conn = connect()
    if conn:
        try:
            # create cursor for executing query
            cursor = conn.cursor()
            # select all students fields
            cursor.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students")
            # fetch all rows returned by the cursor
            students = cursor.fetchall()
            # for each student print all information
            for student in students:
                print(student)
        # on error, print error
        except errors.Error as e:
            print(f"Error: Unable to fetch students: {e}")
        finally:
            # close connection
            cursor.close()
            close_connection(conn)

# function for adding student to database
def addStudent(first_name, last_name, email, enrollment_date):
    # establish connection string
    conn = connect()
    if conn:
        try:
            # create cursor for executing query
            cursor = conn.cursor()
            # insert into students table
            cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
            # commit  the transaction to the database
            conn.commit()
            # print a success message
            print("Student added successfully.")
        # on error, print the error
        except errors.Error as e:
            print(f"Error: Unable to add student: {e}")
            # rollback to undo changes.
            conn.rollback()
        finally:
            # close conneciton
            cursor.close()
            close_connection(conn)

# function for updating student email
def updateStudentEmail(student_id, new_email):
    conn = connect()
    if conn:
        try:
            # establish cursor for updating
            cursor = conn.cursor()
            # update students table with new values matched on student_id
            cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
            # commit the changes
            conn.commit()
            # print success message
            print("Email updated successfully.")
        # on error, print the error
        except errors.Error as e:
            print(f"Error: Unable to update email: {e}")
            # rollback if failure to undo transaction
            conn.rollback()
        finally:
            # close connection
            cursor.close()
            close_connection(conn)

# function for deleting student based on student_id
def deleteStudent(student_id):
    conn = connect()
    if conn:
        try:
            # create cursor for executing delete query
            cursor = conn.cursor()
            # delete from table matched by student_id
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            # commit the transaction
            conn.commit()
            # print success message
            print("Student deleted successfully.")
        # on error, print the error
        except errors.Error as e:
            print(f"Error: Unable to delete student: {e}")
            # rollback transaction on failure.
            conn.rollback()
        finally:
            # close connection
            cursor.close()
            close_connection(conn)

# main function
def main():
    # infinite loop for input, type quit to exit loop.
    while True:
        # list options to user
        print("Type 'get' to call function getAllStudents()")
        print("Type 'add' to call function addStudent(first_name, last_name, email, enrollment_date)")
        print("Type 'update' to call function updateStudentEmail(student_id, email)")
        print("Type 'delete' to call function deleteStudent(student_id)")
        print("Type 'quit' to exit.")

        # accept user input
        user_input = input("Enter option: ")

        # get calls getAllStudents()
        if user_input == 'get':
            getAllStudents()
        # add calls addStudent(first_name, last_name, email, enrollment_date)
        elif user_input == 'add':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            addStudent(first_name, last_name, email, enrollment_date)
        # update calls updateStudentEmail(student_id, new_email)
        elif user_input == 'update':
            student_id = input("Enter student ID: ")
            new_email = input("Enter new email: ")
            updateStudentEmail(student_id, new_email)
        # delete calls deleteStudent(student_id)
        elif user_input == 'delete':
            student_id = input("Enter student ID: ")
            deleteStudent(student_id)
        # quit exits the loop and quits the program.
        elif user_input == 'quit':
            break
        # if none of the options were chosen correctly, the user is reminded of the acceptable options and retries
        else:
            print("Invalid input, please input either 'get', 'add', 'update', 'delete', or 'quit'")

# if ran from file, execute main function
if __name__ == '__main__':
    main()