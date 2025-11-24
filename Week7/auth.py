#Import necessary libraries
import os
import bcrypt
#Hash a password
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode()   
    salt = bcrypt.gensalt()                         
    hashed = bcrypt.hashpw(password_bytes, salt)    
    return hashed.decode()                          


#Verify password
def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode()       
    hashed_bytes = hashed_password.encode()             
    return bcrypt.checkpw(password_bytes, hashed_bytes) 


#Test the functions
if __name__ == "__main__":
    test_password = "SecurePassword12"

    hashed = hash_password(test_password)
    print("Original password:", test_password)
    print("Hashed password:", hashed)
    print("Hash length:", len(hashed))

    print("\nCorrect password:", verify_password(test_password, hashed))
    print("Wrong password:", verify_password("WrongPassword", hashed))


#User data storage
USER_DATA_FILE = "users.txt"

#Check if user exists

def user_exists(username):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                stored_username, _ = line.strip().split(",")
                if stored_username == username:
                    return True
    except FileNotFoundError:
        return False  
    return False


#Register the user in system
def register_user(username, password):
    if user_exists(username):
        return False  

    hashed = hash_password(password)

    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed}\n")

    return True

#Login the user
def login_user(username, password):
    try:
        with open(USER_DATA_FILE, "r") as f:
            for line in f:
                stored_username, stored_hash = line.strip().split(",")
                if stored_username == username:
                    return verify_password(password, stored_hash)
    except FileNotFoundError:
        return False
    return False  
               
#Input validation
def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."

    if " " in username:
        return False, "Username cannot contain spaces."

    if not username.isalnum():
        return False, "Username must only contain letters and numbers."

    return True, ""


def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    if not any(ch.isalpha() for ch in password):
        return False, "Password must contain at least one letter."

    if not any(ch.isdigit() for ch in password):
        return False, "Password must contain at least one number."

    return True, ""

#Add menu display
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
