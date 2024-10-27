#   GeneratorModel Class (concern generating a random password secured for the client for any site/app)

import DAO
import string
import random

from utility.functionUtility import(
    get_password_options, get_boolean_input
)

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH
)

class GeneratorModel:

    def __init__(self, username):
        self.username = username

    def generate_password(self):

        print('*******  Generating a new password  *******')
        do_while = True
        params = {
        "password_length" : None,   # 8 - 128 characters
        "lowercase_alphabet" : False,   # a-z
        "uppercase_alphabet" : False,   # A-Z
        "numbers" : False,  #0-9
        "specials_car" : False, # @!#$(). . .
        "min_numbers" : 0,
        "min_specials_car" : 0
        }

        #   Immitating a "do while" loop
        while do_while:
            # Call print_password_options and get the updated values
            params = get_password_options()
            #   Verify input (at least one option must be true)
            params = self.verify_password(params)

            if get_boolean_input("do you confirm your choices? (Yes/no): "):
                do_while = False

        #   Generate a password with the parameters
     # for x in reversed(params["password_length"]):
     #     if params["numbers"] & params["specials_car"]:

     #     elif

        # Define character pools
        lowercase = string.ascii_lowercase if params["lowercase_alphabet"] else ""
        uppercase = string.ascii_uppercase if params["uppercase_alphabet"] else ""
        numbers = string.digits if params["numbers"] else ""
        specials = "!@#$%^&*()_+-=[]{}|;:',.<>?/" if params["specials_car"] else ""

        # Create a combined pool of characters based on enabled options
        all_chars = lowercase + uppercase + numbers + specials
        password = []

        # Ensure minimum numbers and special characters
        password.extend(random.choices(numbers, k=params["min_numbers"]))
        password.extend(random.choices(specials, k=params["min_specials_car"]))

        # Fill the remaining length with random characters from the enabled pools
        remaining_length = params["password_length"] - len(password)
        if remaining_length > 0:
            password.extend(random.choices(all_chars, k=remaining_length))

        # Shuffle the password to ensure randomness
        random.shuffle(password)

        # Join list into a final password string
        return ''.join(password)

    def verify_password(self, params):
    #   Validate all hash parameters at once.
        validated_params = {}
        
        #   Check if no options has been set to true (means that nothing can be created), then put a-z at least to true
        while(validated_params["lowercase_alphabet"] & validated_params["uppercase_alphabet"] & validated_params["numbers"] & validated_params["specials_car"]):
            print("\n No options has been chosen, retry (at least one true)\n")
            get_password_options(params)

        #   Ensure time cost is within the range of minimum and maximum limits
        validated_params["password_length"] = max(
            min(int(params["password_length"]) if params["time_cost"] else DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH), MIN_PASSWORD_LENGTH
        )

        #   Ensure the minimum numbers don't exceeds the password length
        #   Default settings if no input is provided is 1/4 the length of the password
        validated_params["min_numbers"] = max(
            min(int(params["min_numbers"]) if params["min_numbers"] else (validated_params["password_length"]/4), MAX_PASSWORD_LENGTH), MIN_PASSWORD_LENGTH
        )

        #   Ensure the minimum specials characters don't exceeds the password length
        validated_params["min_specials_car"] = max(
            min(int(params["min_specials_car"]) if params["min_specials_car"] else (validated_params["password_length"]/4), MAX_PASSWORD_LENGTH), MIN_PASSWORD_LENGTH
        )

        #   adjust the password if there's more numbers and specials characters than the password length
        # TODO : Additionner les valeurs et mitigué ensuite
        added_options_numbers = validated_params["min_numbers"] + validated_params["min_specials_car"]
        if added_options_numbers > validated_params["password_length"]:
            scale_factor  = (validated_params["password_length"] / added_options_numbers)
            validated_params["min_numbers"] = validated_params["min_numbers"] * scale_factor
            validated_params["min_specials_car"] = validated_params["min_specials_car"] * scale_factor
            rounded_value_1 = round(validated_params["min_numbers"] * scale_factor)
            rounded_value_2 = round(validated_params["min_specials_car"] * scale_factor)


            round_sum_params = validated_params["min_numbers"] + validated_params["validated_params"]
            print("should be max_length : ", round_sum_params)

            #   More security if one numbers if off by one
            if round_sum_params < validated_params["password_length"]:
                #   Add 1 to the value with the higher decimal component
                if (validated_params["min_numbers"] - rounded_value_1) > (validated_params["min_specials_car"] - rounded_value_2):
                    rounded_value_1 += 1
                else:
                    rounded_value_2 += 1
            elif round_sum_params > validated_params["password_length"]:
                # Subtract 1 from the value with the higher decimal component
                if (validated_params["min_numbers"] - rounded_value_1) > (validated_params["min_specials_car"] - rounded_value_2):
                    rounded_value_1 -= 1
                else:
                    rounded_value_2 -= 1

            validated_params["min_numbers"] = rounded_value_1
            validated_params["min_specials_car"] = rounded_value_2
        return validated_params
            

