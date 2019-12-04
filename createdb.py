import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#lock: khoa do dang nhap qua nhieu, 0 la unlock, 1 la lock
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,username text, password text, lock int, role int)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS otp_users (username text, OTP int, start int, end int)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS logs (username text, wrongnum int)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS baiviet (id INTEGER PRIMARY KEY,username text, tittle text, linkpost text, content text, comment text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS roledetail (idrole int, rolename text)"
cursor.execute(create_table)


admin1 = ('loc','tra',0,1)
mod2 = ('tra','loc',0,2)
user3 = ('thanh','ngoc',0,3)
insert = "INSERT INTO users VALUES(NULL,?,?,?,?)"

cursor.execute(insert, admin1)
cursor.execute(insert,mod2)
cursor.execute(insert,user3)

role1 = (1, 'admin')
role2 = (2, 'mod')
role3 = (3, 'user')

insert = "INSERT INTO roledetail VALUES(?,?)"
cursor.execute(insert,role1)
cursor.execute(insert,role2)
cursor.execute(insert,role3)

# select_query = "SELECT * FROM users"
#
# for row in cursor.execute(select_query):
#     print(type(row[2]))

connection.commit()
connection.close()




action = {{url_for('baiviet', linkpost = '{{linkpost}}' )}},