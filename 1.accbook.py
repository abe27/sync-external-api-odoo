import pyodbc
import requests
import json

# Set your SQL Server connection parameter
server = '192.168.10.6'
database = 'formula'
username = 'fm1234'
password = 'x2y2'

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
# Establish a connection
connection = pyodbc.connect(connection_string)
# Create a cursor to execute queries
cursor = connection.cursor()

# Example query
query = 'select a.FCSKID,a.FCCODE,a.FCNAME,a.FCNAME2 from ACCBOOK a '

url = "http://localhost:8081/api/vcsgroup/accbook"
try:
    # Execute the query
    cursor.execute(query)
    # Fetch all rows
    rows = cursor.fetchall()

    # Process the data
    for r in rows:
        payload = json.dumps({
            "params": {
                "account_book_id": str(r[0]).strip(),
                "account_book_code": str(r[1]).strip(),
                "name": str(r[2]).strip(),
                "description": str(r[3]).strip(),
                "is_active": "true",
            }
        })

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print("{} {}".format(str(r[0]).strip(), response.status_code))

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()