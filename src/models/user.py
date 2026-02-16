from src.data.user_repo import create_user, get_user_id
# Checks if the user exists. If not, a new user is registered
def createUser():
    while True:
        username = input()
        if get_user_id(username) == None:
            create_user(username)
            print("Registered")
            break
        else:
            print("Try again")
        