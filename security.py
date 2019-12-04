from user import User

def authenticate(username, password):
    user = User.find_by_user(username)
    if user and user.password == password:
        return user

