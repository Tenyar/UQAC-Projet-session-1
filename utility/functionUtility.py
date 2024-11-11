#   Utility fonctions for GeneratorController
#   Involve mainly and only print/input statements
def get_password_options(params):

    print('test')
    params["password_length"] = input("Enter the password length (8-128): ") 
    if not params["password_length"]:
        params["password_length"] = 16
    params["lowercase_alphabet"] = get_boolean_input("Include lowercase letters? (y/n): ")
    params["uppercase_alphabet"] = get_boolean_input("Include uppercase letters? (y/n): ")
    params["numbers"] = get_boolean_input("Include numbers? (y/n): ")
    params["specials_car"] = get_boolean_input("Include special characters? (y/n): ")
    #   if one of these options is true
    params["min_numbers"] = input("Minimum number of digits: ")
    if not params["min_numbers"]:
        params["min_numbers"] = 4
    params["min_specials_car"] = input("Minimum number of special characters: ")
    if not params["min_specials_car"]:
        params["min_specials_car"] = 4
    
    #   Make sure the values are int
    params["password_length"] = int(params["password_length"])
    params["min_numbers"] = int(params["min_numbers"])
    params["min_specials_car"] = int(params["min_specials_car"])
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