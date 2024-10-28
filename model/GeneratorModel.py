#   GeneratorModel Class (concern generating a random password secured for the client for any site/app)

import string
import random

from utility.functionUtility import(
    get_password_options, get_boolean_input
)

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH
)
from model.DAO import DAO

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
        "min_numbers" : 0,  # minimum of numbers present in the password
        "min_specials_car" : 0  # minimum of specials characters present in the password
        }

        #   Immitating a "do while" loop
        while do_while:
            # Call print_password_options and get the updated values
            params = get_password_options(params)
            #   Verify input (at least one option must be true)
            params = self.verify_password(params)
            #   Display password settings
            print('--------------------------')
            for key, value in params.items():
                 print(f"value {key} : {value}")
            print('--------------------------')

            if get_boolean_input("do you confirm your choices? (Yes/no): "):
                do_while = False
        print("Params after verify_password:", params)
        #   Generate a password with the parameters
     # for x in reversed(params["password_length"]):
     #     if params["numbers"] & params["specials_car"]:

     #     elif

        # Define character pools
        print('TEST 1   TEST 1')
        lowercase = string.ascii_lowercase if params["lowercase_alphabet"] == True else ""
        print('TEST 2   TEST 2')
        uppercase = string.ascii_uppercase if params["uppercase_alphabet"] == True else ""
        numbers = string.digits if params["numbers"] == True else ""
        specials = "!@#$%^&*()_+-=[]{}|;:',.<>?/" if params["specials_car"] == True else ""

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
        validated_params = params
        #   Check if no options has been set to true (means that nothing can be created), then put a-z at least to true
        while(params["lowercase_alphabet"] == False & params["uppercase_alphabet"] == False & params["numbers"] == False & params["specials_car"] == False):
            print("\n No options has been chosen, retry (at least one true)\n")
            get_password_options(params)

        #   Ensure time cost is within the range of minimum and maximum limits
        validated_params["password_length"] = max(
            min(int(params["password_length"]) if params["password_length"] else DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH), MIN_PASSWORD_LENGTH
        )

        #   Ensure the minimum numbers don't exceeds the password boundaries
        #   Default settings if the input is < 0 (incorrect) or is beyond the maximum capacity
        if params["numbers"]:
            print('test', params["min_numbers"])
            # Clamp min_numbers within the range [0, password_length]
            validated_params["min_numbers"] = max(0, min(int(params["min_numbers"]), validated_params["password_length"]))
        else:
            validated_params["min_numbers"] = params["min_numbers"]
        
        #   Ensure the minimum specials characters don't exceeds the password boundaries
        if params["numbers"]:
            print('test', params["min_numbers"])
            # Clamp min_numbers within the range [0, password_length]
            validated_params["min_specials_car"] = max(0, min(int(params["min_specials_car"]), validated_params["password_length"]))
        else:
            validated_params["min_specials_car"] = params["min_specials_car"]


        #   adjust the password if there's more numbers and specials characters than the password length
        # TODO : Additionner les valeurs et mitigué ensuite
        added_options_numbers = validated_params["min_numbers"] + validated_params["min_specials_car"]
        if added_options_numbers > validated_params["password_length"]:
            scale_factor  = (validated_params["password_length"] / added_options_numbers)
            validated_params["min_numbers"] = validated_params["min_numbers"] * scale_factor
            validated_params["min_specials_car"] = validated_params["min_specials_car"] * scale_factor
            rounded_value_1 = round(validated_params["min_numbers"] * scale_factor)
            rounded_value_2 = round(validated_params["min_specials_car"] * scale_factor)

            round_sum_params = rounded_value_1 + rounded_value_2
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
            

