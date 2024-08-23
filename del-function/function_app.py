import azure.functions as func
import MySQLdb
import json
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing DELETE request.')

    # Get the 'id' parameter from the request
    employee_id = req.params.get('id')

    if not employee_id:
        return func.HttpResponse(
            json.dumps({"message": "Missing ID parameter"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        # Establish MySQL connection using individual parameters
        conn = MySQLdb.connect(
            host="localhost",
            user="root",
            password="cogniwide@2024",
            database="pro_1",
            port=3306
        )
        
        cursor = conn.cursor()

        # Execute delete query
        delete_query = "DELETE FROM demo_app_employee WHERE id = %s"
        cursor.execute(delete_query, (employee_id,))
        conn.commit()

        if cursor.rowcount > 0:
            return func.HttpResponse(
                json.dumps({"message": f"Employee with ID {employee_id} deleted successfully."}),
                status_code=200,
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                json.dumps({"message": "Employee not found."}),
                status_code=404,
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
