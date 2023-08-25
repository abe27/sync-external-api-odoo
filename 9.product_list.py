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
query = "select r.FCTYPE,r.FCCODE,r.FCUM,'TEST',r.FNPRICE from PROD r order by FCCODE"

url = "http://localhost:8081/api/vcsgroup/productlist"
try:
    # Execute the query
    cursor.execute(query)
    # Fetch all rows
    rows = cursor.fetchall()

    # Process the data
    i = 0
    for r in rows:
        payload = json.dumps({
            "params": {
                "type": str(r[0]).strip(),
                "product": str(r[1]).strip(),
                "unit": str(r[2]).strip(),
                "whs": str(r[3]).strip(),
                "price": str(r[4]).strip(),
                "is_active": "true",
            }
        })

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print("{}. {} {}".format(str(i), str(r[0]).strip(), response.status_code))
        i += 1

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
