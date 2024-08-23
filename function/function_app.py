import azure.functions as func
import MySQLdb
import json
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing POST request to create an employee.')

    try:
        req_body = req.get_json()
        fullname = req_body.get('fullname')
        age = req_body.get('age')
        designation = req_body.get('designation')
        salary = req_body.get('salary')

        if not (fullname and age and designation and salary):
            return func.HttpResponse(
                json.dumps({"message": "Missing one or more employee fields"}),
                status_code=400,
                mimetype="application/json"
            )

        # Establish MySQL connection using individual parameters
        conn = MySQLdb.connect(
            host="localhost",
            user="root",
            password="cogniwide@2024",
            database="pro_1",
            port=3306
        )
        
        cursor = conn.cursor()

        # Insert new employee record
        insert_query = """
        INSERT INTO demo_app_employee (fullname, age, designation, salary) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (fullname, age, designation, salary))
        conn.commit()

        return func.HttpResponse(
            json.dumps({"message": f"Employee {fullname} created successfully."}),
            status_code=201,
            mimetype="application/json"
        )

    except MySQLdb.Error as e:
        logging.error(f"Database error occurred: {str(e)}")
        return func.HttpResponse(
            json.dumps({"message": "An unexpected error occurred.", "error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
    finally:
        cursor.close()
        conn.close()
