import bcrypt
import os

USER_DATA_FILE = 'users.txt'

# STEP 4: Hash Password Function
def hash_password(password):
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')
    # Generate a salt and salt the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to string to store in a text file
    return hashed.decode('utf-8')

# STEP 5: Verify Password Function
def verify_password(plain_text_password, hashed_password):
    # Encode the plain text password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    # Verify the password
    return bcrypt.checkpw(password_bytes, hashed_bytes) # bycrypt.checkpw handles extracting salt and comapring then returns True or False

# STEP 7: Registeration User Function with week 8 extension for role
def register_user(username, password, role='user'):
    '''Registers a new user by storing their username, hashed password and role.'''
    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password},{role}\n")
    print(f"User {username} registered successfully.")

# STEP 8: Check if User Exists Function
def user_exists(username):
    '''Checks if a user already exists in the user data file.'''
    # Handle case where file does not exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False
    # Read through the file to check each line for existing username
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            user,hash = line.strip().split(',',1)
            if user == username:
                return True
    return False

# STEP 9: Login Function
def login_user(username, password):
    '''Logs in a user by verifying their username and password.'''
    # Handle the case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("No users registered yet.")
        return False
    # Search for the username in the file
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            user,hash = line.strip().split(',',1)
            # If username matches, verify the password
            if user == username:
                if verify_password(password, hash):
                    print(f"User {username} logged in successfully.")
                    return True
                else:
                    print("Incorrect password.")
                    return False
    print("Username not found.")
    return False

# STEP 10: Input Validation Function
def validate_username(username):
    '''Validates the username format.'''
    if not username or len(username) < 3:
        return(False,"Username must be at least 3 characters long.")
    return (True, "is valid")

def validate_password(password):
    '''Validates password strength.'''
    if not password or len(password) < 8:
        return (False, "Password must be at least 8 characters long.")
    
    has_upper = any(i.isupper() for i in password)
    has_lower = any(i.islower() for i in password)
    has_digit = any(i.isdigit() for i in password)
    
    if not has_upper:
        return (False, "Password must contain at least one uppercase letter.")
    if not has_lower:
        return (False, "Password must contain at least one lowercase letter.")
    if not has_digit:
        return (False, "Password must contain at least one digit.")
    
    return (True, "is valid")


# STEP 11: Implementing the Main Menu
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
        
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

             # Get password
            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm your password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Get role
            role = input("Enter role (user/admin/analyst): ").strip().lower()
            if role not in ['user', 'admin', 'analyst', '']:
                print("Error: Invalid role. Please enter 'user', 'admin', or 'analyst'.")
                continue

            # Check if user already exists
            if user_exists(username):
                print(f"Error: Username {username} already exists.")
                continue
            
            # Register the user
            register_user(username, password, role if role else 'user')
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
        
if __name__ == "__main__":
    main()