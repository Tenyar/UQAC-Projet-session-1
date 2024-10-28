#   Utility fonctions for GeneratorController
#   Involve mainly and only print/input statements
def get_password_options(params):
    params["password_length"] = int(input("Enter the password length (8-128): "))
    params["lowercase_alphabet"] = get_boolean_input("Include lowercase letters? (y/n): ")
    params["uppercase_alphabet"] = get_boolean_input("Include uppercase letters? (y/n): ")
    params["numbers"] = get_boolean_input("Include numbers? (y/n): ")
    params["specials_car"] = get_boolean_input("Include special characters? (y/n): ")
    #   if one of these options is true
    params["min_numbers"] = int(input("Minimum number of digits: ")) if params["numbers"] == True else 0
    params["min_specials_car"] = int(input("Minimum number of special characters: ")) if params["specials_car"] == True else 0

    # Return all the values
    return params

def get_boolean_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()  # Stripping extra spaces
        if user_input in ['yes', 'y', 'true', 't', '1']:  # Interpreting affirmative responses
            return True
        elif user_input in ['no', 'n', 'false', 'f', '0']:  # Interpreting negative responses
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")  # Retry on invalid input