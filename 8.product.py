import pyodbc
import requests
import json

# Set your SQL Server connection parameter
server = '192.168.20.9'
database = 'Formula'
username = 'fm1234'
password = 'x2y2'

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;'
# Establish a connection
connection = pyodbc.connect(connection_string)
# Create a cursor to execute queries
cursor = connection.cursor()
# Example query
query = "select r.FCCODE,r.FCNAME,r.FCNAME2 from PROD r where r.FCTYPE in ('2','3','4','5') order by FCCODE"

url = "http://localhost:8081/api/vcsgroup/product"
try:
    # Execute the query
    cursor.execute(query)
    # Fetch all rows
    rows = cursor.fetchall()

    # Process the data
    for r in rows:
        payload = json.dumps({
            "params": {
                "code": str(r[0]).strip(),
                "name": str(r[1]).strip(),
                "description": str(r[2]).strip(),
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
