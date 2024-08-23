import azure.functions as func
import logging
import MySQLdb
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing GET request to retrieve employee(s).')

    # Define the MySQL connection parameters and establish the connection
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        password="cogniwide@2024",
        database="pro_1",
        port=3306
    )

    cursor = conn.cursor()

    # SQL query to fetch employees
    query = "SELECT * FROM DEMO_app_employee"
    cursor.execute(query)
    rows = cursor.fetchall()
    employees = []

    # Process the query result
    for row in rows:
        employee = {
            "id": row[0],
            "fullname": row[1],
            "age": row[2],
            "designation": row[3],
            "salary": float(row[4])  # Convert Decimal to float
        }
        employees.append(employee)
    
    logging.info('Employees: {}'.format(employees))

    # Close the connection
    conn.close()

    # Return the employees as JSON
    return func.HttpResponse(
        json.dumps(employees),
        status_code=200,
        mimetype="application/json"
    )
