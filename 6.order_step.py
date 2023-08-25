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
isRead = models.execute_kw(odoo_db, uid, odoo_password, 'vcsgroup.order_step', 'check_access_rights', [
                           'read'], {'raise_exception': False})
if isRead:
    typeName = [
        {
            "step_id": "1",
            "name": "None",
            "description": "None",
            "is_active": True,
        },
        {
            "step_id": "P",
            "name": "Paid",
            "description": "Paid",
            "is_active": True,
        }
    ]

    for i in typeName:
        id = models.execute_kw(odoo_db, uid, odoo_password, 'vcsgroup.order_step', 'create', [i])
        print(id)
