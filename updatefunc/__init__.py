import azure.functions as func
import logging
import pyodbc
import json
from decimal import Decimal
import os

conn_str = os.getenv("projectdb")

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a PUT request to update an employee.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in request body",
            
        )
    
   
    required_fields = ['id', 'fullname', 'age', 'salary', 'designation']
    for field in required_fields:
        if field not in req_body:
            return func.HttpResponse(
                f"Missing required field: {field}",
               
            )

    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            
            
            update_query = """
            UPDATE DEMO_app_employee
            SET fullname = ?, age = ?, salary = ?, designation = ?
            WHERE ID = ?
            """
            cursor.execute(update_query, 
                           req_body['fullname'], 
                           req_body['age'], 
                           req_body['salary'], 
                           req_body['designation'],
                           req_body['id'])
            conn.commit()
            
           
            if cursor.rowcount == 0:
                return func.HttpResponse(
                    f"No employee found with ID {req_body['id']}",
                    
                )

            return func.HttpResponse(
                "Employee updated successfully",
                
            )
    except pyodbc.Error as e:
        logging.error(f"Database error: {str(e)}")
        return func.HttpResponse(
            f"Failed to update employee: {str(e)}",
            
        )
