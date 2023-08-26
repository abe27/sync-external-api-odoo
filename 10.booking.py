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
query = "select b.FCREFTYPE,b.FCSKID,b.FCCODE,b.FCPREFIX,b.FCNAME,b.FCNAME2,b.FCWHOUSE,b.FCTOWHOUSE  from BOOK b order by b.FCREFTYPE"

url = "http://localhost:8081/api/vcsgroup/booking"
try:
    # Execute the query
    cursor.execute(query)
    # Fetch all rows
    rows = cursor.fetchall()

    # Process the data
    for r in rows:
        payload = json.dumps({
            "params": {
                "ref_type_id": str(r[0]).strip(),
                "booking_id": str(r[1]).strip(),
                "booking_code": str(r[2]).strip(),
                "prefix": str(r[3]).strip(),
                "name": f"{str(r[2]).strip()}-{str(r[4]).strip()}",
                "description": str(r[5]).strip(),
                "from_whs_id": str(r[6]).strip(),
                "to_whs_id": str(r[7]).strip(),
                "is_active": "true",
            }
        })

        print(payload)

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
