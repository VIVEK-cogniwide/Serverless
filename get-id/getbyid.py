import azure.functions as func
import logging
import MySQLdb
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing GET request to retrieve an employee.')

    employee_id = req.params.get('id')
    if not employee_id:
        return func.HttpResponse(
            "Missing required query parameter: id",
            status_code=400
        )

    try:
        # Establish the connection
        conn = MySQLdb.connect(
            host="localhost",
            user="root",
            password="cogniwide@2024",
            database="pro_1",
            port=3306
        )
        with conn:
            cursor = conn.cursor()

            # Retrieve the employee details
            cursor.execute("SELECT * FROM demo_app_employee WHERE ID = %s", (employee_id,))
            row = cursor.fetchone()

            if row:
                employee = {
                    "id": row[0],
                    "fullname": row[1],
                    "age": row[2],
                    "salary": row[3],
                    "designation": row[4]
                }
                return func.HttpResponse(
                    json.dumps(employee),
                    mimetype="application/json",
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    f"Employee with ID {employee_id} not found.",
                    status_code=404
                )
    except MySQLdb.Error as e:
        logging.error(f"Database error: {str(e)}")
        return func.HttpResponse(
            f"Failed to retrieve employee: {str(e)}",
            status_code=500
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            "An unexpected error occurred.",
            status_code=500
        )
