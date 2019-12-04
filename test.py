import sqlite3
import time

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
select_query = "SELECT * FROM users"

lock = 1
update_query = "UPDATE users set lock = 0 WHERE lock = ?"
cursor.execute(update_query, (lock,))

# for row in cursor.execute(select_query):
#      print(row)
# delete = "DELETE FROM logs"
# cursor.execute(delete)
# user3 = ('ha','1234',0,2)
# # insert = "INSERT INTO users VALUES(NULL,?,?,?,?)"
# # cursor.execute(insert, user3)
# query = "DELETE FROM users WHERE username = ?"
# username = "ha"
# cursor.execute(query,(username,))
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()

# print(int(time.time()))
# time.sleep(30)
#print(int(time.time()))