import sqlite3

class User:
    def __init__(self,_id,username,password,lock,role):
        self.id = _id
        self.username = username
        self.password = password
        self.lock = lock
        self.role = role

    @classmethod
    def find_by_user(cls,username):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users where username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connect.close()
        return user

    @classmethod
    def find_by_id(cls,id):
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        query = "SELECT * FROM users where id = ?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connect.close()
        return user


