import sqsp
import json
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os


sqsp_api_key = os.environ.get('sqsp_api_key')

# Connect to the database using environment variables. 
mydb = mysql.connector.connect(
    host=os.environ.get('mySQL_host'),
    port=os.environ.get('mySQL_port'),
    user=os.environ.get('mySQL_user'),
    password=os.environ.get('mySQL_password'),
    database=os.environ.get('mySQL_database')
)

orders = sqsp.all_orders(sqsp_api_key) 

keys = ""
values = ""

# Create a list of keys for insertion into the database. Adds discountCode as this will be used for affiliate tracking. 
allKeys = list(orders[0].keys())
allKeys.pop(0)
allKeys.append("discountCode")

#formates the keys for insertion into the database.
for x in allKeys:
    keys+= x + ", "
    values+= "%s, "

keys = keys[:-2]
values = values[:-2]

mycursor = mydb.cursor()
tableName = "sqsp"
inserts = []


# iterates through all orders and creates a big insert statement that will be used to insert all orders into the database.
for x in orders:
    line = []
    for y in allKeys:
        data = x.get(y)
        if(type(x.get(y)) == dict or type(x.get(y)) == list):
            data = json.dumps(data)
        line.append(data)

    if(len(x.get("discountLines")) > 0):
        discountCode = x.get("discountLines")[0]
        discountCode = discountCode.get("promoCode")
        line.pop()
        line.append(discountCode)
    else:
        line.pop()
        line.append("null")
        
    checkStatement = "SELECT * FROM " + tableName + " WHERE orderNumber = " + x.get("orderNumber")
    mycursor.execute(checkStatement)

    dbLineItem = mycursor.fetchone()

    if(dbLineItem != None):
        if(dbLineItem[8] != x.get("fulfillmentStatus")):
            # print(json.dumps(x.get("fulfilledOn")))
            sql = "UPDATE " + tableName + " SET fulfillmentStatus = '"+ x.get("fulfillmentStatus") + "', fulfillments = '" + json.dumps(x.get("fulfillments")) + "', fulfilledOn = '" + x.get("fulfilledOn") + "' WHERE orderNumber = " + x.get("orderNumber")
            mycursor.execute(sql)
            mydb.commit()

    if(dbLineItem == None):
        line = tuple(line)
        inserts.append(line)


#inserts all the orders into the database using the big insert statement.
if(len(inserts) > 0):
    # print(len(inserts))
    sql = "INSERT INTO " + tableName +  " (" + keys + ") VALUES (" + values + ")"
    # print(sql)
    # print(inserts)
    mycursor.executemany(sql, inserts)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
