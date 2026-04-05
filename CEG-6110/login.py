#  usernames 8 characters exactly, all lowercase. passwords 12 characters exactly, 1 upper, 1 lower, 1 number, 1 symbol/special char
login_db = {
    "student1" : "Password123$",
    "student2" : "Password234%",
    "student3" : "Password345^",
    "student4" : "Password456&",
    "student5" : "Password567*",
    "faculty1" : "Faculty1234%",
    "faculty2" : "Faculty2345^",
    "faculty2" : "Faculty3456&",
    "adminadmin" : "Adminadmin123$"
}

# dictionary to connect the account to its account type of student/faculty/admin
account_types = {
    "student1" : "student",
    "student2" : "student",
    "student3" : "student",
    "student4" : "student",
    "student5" : "student",
    "faculty1" : "faculty",
    "faculty2" : "faculty",
    "faculty2" : "faculty",
    "adminadmin" : "admin"
}

def authenticate(username, password):
    """Takes in the username and password and returns True if the password is correct. 
    Returns 0 if no username found. Returns -1 if incorrect password 
    """
    username_found = login_db.get(username, 0)  # sets username_found to the corresponding password if the username is found. otherwise it is set to 0
    if username_found != 0:
        if password == username_found:
            print("Login successful!")
            return True
        else:
            print("Login failed. Incorrect password")   # this might need to be turned into a message string to return?
            return False
    else:
        print("Login failed. Username not found")   # this might need to be turned into a message string to return?
        return False

def get_account_type(username):
    """Returns the account type for the given username, or None if not found."""
    return account_types.get(username)