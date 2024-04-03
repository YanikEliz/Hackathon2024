import hashlib
import random
import string

# Define password strength levels
WEAK = "Weak"
MODERATE = "Moderate"
STRONG = "Strong"

# Simple in-memory database
user_database = {}


# Function to assess password strength
def assess_password_strength(password):
    length = len(password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)

    if length < 8 or not (
        has_upper and has_lower and has_digit and has_special
    ):
        return WEAK
    elif length < 12 or not has_special:
        return MODERATE
    else:
        return STRONG


# Function to estimate time to crack password
def estimate_crack_time(password_strength):
    if password_strength == WEAK:
        return "Seconds to minutes"
    elif password_strength == MODERATE:
        return "Hours to days"
    elif password_strength == STRONG:
        return "Years to centuries"


# Function to generate strong password
def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


# Function to store username and hashed password
def register(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_database[username] = hashed_password


# Function to validate login credentials
def login(username, password):
    if username in user_database:
        hashed_password = user_database[username]
        if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
            print("Login successful!")
            return True
    print("Login failed!")
    return False


# Test the functions
if __name__ == "__main__":
    menu_option = input(
        "Select A for user registration and B for login and Q to quit: "
    )
    print("")
    locked_ID = []
    while menu_option not in ["Q", "q"]:
        if menu_option.upper() == "A":
            user_id = input("Enter a user ID between 6 and 12 characters: ")
            while not (6 <= len(user_id) <= 12):
                print("User ID length is out of bounds, try again!")
                user_id = input(
                    "Enter a user ID between 6 and 12 characters: "
                )
            if user_id in user_database:
                print("Please retry, user ID already exists.")
                user_id = input(
                    "Enter a user ID between 6 and 12 characters: "
                )
            gen_option = input(
                "Do you want me to generate a strong password for you? "
            )
            if gen_option.lower() in ["yes", "y"]:
                gen_password = generate_strong_password()
                print("Generated strong password:", gen_password)
                register(user_id, gen_password)
                print(
                    "You are now registered with a generated strong password!"
                )
                menu_option = input(
                    "Select A for user registration and B for login and Q to quit: "
                )
            elif gen_option.lower() in ["no", "n"]:
                user_pass = input("Please input a password: ")
                while assess_password_strength(user_pass) != STRONG:
                    print(
                        f"Password strength is {assess_password_strength(user_pass)}, please try again as can be cracked in {estimate_crack_time(user_pass)}!"
                    )
                    print(
                        "Make sure you have at least one upper case, one lower case, one digit and one special character and is between 8 and 18 characters"
                    )
                    user_pass = input("Please input a password: ")
                register(user_id, user_pass)
                print("You are now registered with the provided password!")
                menu_option = input(
                    "Select A for user registration and B for login and Q to quit: "
                )
            else:
                print("Invalid response please try again!")

        elif menu_option.upper() == "B":
            pass_attempts = []
            user_ID = input("Please input user ID: ")
            while user_ID in locked_ID:
                print(
                    f"{user_ID} locked. Call tech support for further assistance!"
                )
                user_ID = input("Try a new user ID: ")
            pass_attempts.append(input("Enter Password: "))
            if user_ID not in user_database:
                print("User ID not registered!")
                menu_option = input(
                    "Select A for user registration and B for login and Q to quit: "
                )
            if not login(user_ID, pass_attempts[0]):
                pass_attempts.append(input("Try Password Again: "))
                if not login(user_ID, pass_attempts[1]):
                    pass_attempts.append(input("Last password attempt: "))
                    if not login(user_ID, pass_attempts[2]):
                        locked_ID.append(user_ID)
                        print(f"You are now locked out of account {user_ID}")
            else:
                menu_option = input(
                    "Select A for user registration and B for login and Q to quit: "
                )
        else:
            print("Invalid input please try again!\n")
            menu_option = input(
                "Select A for user registration and B for login and Q to quit: "
            )