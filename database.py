import mysql.connector

# Enter MySQL login info here.
pw = ''
host = ''
user = ''

config = {
    'user': user,
    'password': pw,
    'host': host
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

