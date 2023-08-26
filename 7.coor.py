import xmlrpc.client
import pyodbc
import requests
import json


odoo_url = "http://localhost:8081"
odoo_db = "odoo_db"
odoo_username = 'admin'
odoo_password = "admin"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
print(common.version())


uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))
isRead = models.execute_kw(odoo_db, uid, odoo_password, 'res.partner', 'check_access_rights', [
                           'read'], {'raise_exception': False})
if isRead:
    # isCompany = models.execute_kw(db, uid, password, 'res.partner', 'search', [
    #                               [['is_company', '=', True]]])
    # print(isCompany)


    # ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [
    #                         [['is_company', '=', True]]], {'limit': 1})
    # [record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])
    # # count the number of fields fetched by default
    # print(len(record))
    # print(record)

    # fieldsGet = models.execute_kw(db, uid, password, 'res.partner', 'fields_get', [
    # ], {'attributes': ['string']})

    # print(fieldsGet)

    # id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    #         'name': 'บมจ.เอเซียเมทัล',
    #         "display_name": 'บมจ.เอเซียเมทัล',
    #         "company_name": 'AMP',
    #         "is_company": True,
    #         "street": '55/1 ม.2 ซ.วัดหนามแดง ถ.ศรีนครินทร์ ต.บางแก้ว อ.บางพลี จ.สมุทรปราการ',
    #         "street2": "-",
    #         "phone": '02-383-4100',
    #         "mobile": "-",
    #         "email": '',
    #         "vat": "-",
    #     }])
    # print(id)


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
    query = 'select c.FCNAME,c.FCSNAME2,c.FCCODE,c.FMMEMDATA,c.FCTEL,c.FCEMAIL from COOR c'
    # Execute the query
    cursor.execute(query)
    # Fetch all rows
    rows = cursor.fetchall()
    for r in rows:
        print(r)
        # # # Create new Record
        id = models.execute_kw(odoo_db, uid, odoo_password, 'res.partner', 'create', [{
            'name': str(r[0]).strip(),
            "display_name": str(r[1]).strip(),
            "company_name": str(r[2]).strip(),
            "is_company": True,
            "street": str(r[3]).strip(),
            "street2": "-",
            "phone": str(r[4]).strip(),
            "mobile": "-",
            "email": str(r[5]).strip(),
            "vat": "-",
        }])
        print(id)
