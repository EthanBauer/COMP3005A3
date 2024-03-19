import psycopg
from psycopg import errors

def connect():
    try:
        conn = psycopg.connect(
            dbname="Assignment3",
            user="postgres",
            password="Hannah14!",
            host="localhost",
            port="5432"
        )
        return conn
    except errors.Error as e:
        print(f"Error: Unable to connect to the database: {e}")
        return None

def close_connection(conn):
    try:
        conn.close()
        print("Connection closed.")
    except errors.Error as e:
        print(f"Error: Unable to close connection: {e}")

def getAllStudents():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students")
            students = cursor.fetchall()
            for student in students:
                print(student)
        except errors.Error as e:
            print(f"Error: Unable to fetch students: {e}")
        finally:
            cursor.close()
            close_connection(conn)

def addStudent(first_name, last_name, email, enrollment_date):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
            conn.commit()
            print("Student added successfully.")
        except errors.Error as e:
            print(f"Error: Unable to add student: {e}")
            conn.rollback()
        finally:
            cursor.close()
            close_connection(conn)

def updateStudentEmail(student_id, new_email):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
            conn.commit()
            print("Email updated successfully.")
        except errors.Error as e:
            print(f"Error: Unable to update email: {e}")
            conn.rollback()
        finally:
            cursor.close()
            close_connection(conn)

def deleteStudent(student_id):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            print("Student deleted successfully.")
        except errors.Error as e:
            print(f"Error: Unable to delete student: {e}")
            conn.rollback()
        finally:
            cursor.close()
            close_connection(conn)

# Example usage:

def main():
    while True:
        print("Type 'get' to call function getAllStudents()")
        print("Type 'add' to call function addStudent(first_name, last_name, email, enrollment_date)")
        print("Type 'update' to call function updateStudentEmail(student_id, email)")
        print("Type 'delete' to call function deleteStudent(student_id)")
        print("Type 'quit' to exit.")

        user_input = input("Enter option: ")

        if user_input == 'get':
            getAllStudents()
        elif user_input == 'add':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            addStudent(first_name, last_name, email, enrollment_date)
        elif user_input == 'update':
            student_id = input("Enter student ID: ")
            new_email = input("Enter new email: ")
            updateStudentEmail(student_id, new_email)
        elif user_input == 'delete':
            student_id = input("Enter student ID: ")
            deleteStudent(student_id)
        elif user_input == 'quit':
            break
        else:
            print("Invalid input, please input either 'get', 'add', 'update', 'delete', or 'quit'")

if __name__ == '__main__':
    main()