#!/usr/bin/env python3
get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT * FROM users;")
print(cursor.description)
for row in cursor:
    print(row)
cursor.close()
db.close()
