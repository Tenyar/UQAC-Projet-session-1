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
        #   Parameters for generating a passwords
        lowercase_pool = None   #   Define a lowercase character pool
        uppercase_pool = None   #   Define an upper character pool
        numbers_pool  = None    #   Define a pool of number
        specials_pool = None    #   Define a pool of number
        all_chars = None    #   Create a combined pool of characters based on enabled options
        password = None     #   Where all the characters/numbers/specials are stored


        #   Immitating a "do while" loop
        while do_while:
            #   Call print_password_options and get the updated values
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
        lowercase_pool = string.ascii_lowercase if params["lowercase_alphabet"] == True else ""
        uppercase_pool = string.ascii_uppercase if params["uppercase_alphabet"] == True else ""
        numbers_pool  = string.digits if params["numbers"] == True else ""
        specials_pool = "!@#$%^&*()_+-=[]{}|;:',.<>?/" if params["specials_car"] == True else ""

        
        all_chars = lowercase_pool + uppercase_pool
        password = []

        #   Ensure minimum numbers and special characters
        if numbers_pool:
            chosen_numbers = random.choices(numbers_pool, k=params["min_numbers"])
            password.extend(chosen_numbers)
            #print("Chosen numbers:", chosen_numbers)

        if specials_pool:
            chosen_specials = random.choices(specials_pool, k=params["min_specials_car"])
            password.extend(chosen_specials)
            #print("Chosen specials:", chosen_specials)

        remaining_length = params["password_length"] - len(password)
        if remaining_length < 0:
            print("Error: Minimum character requirements exceed password length.")
            return None

        if remaining_length > 0:
        #   Fill the remaining length with random characters from the enabled pools
            remaining_chars = random.choices(all_chars, k=remaining_length)
            password.extend(remaining_chars)
            print("Remaining chars:", remaining_chars)  # Debug line

        #   Shuffle the password to ensure randomness
        random.shuffle(password)
        #   Join list into a final password string with no separator between each characters
        final_password = ''.join(password)
        return final_password


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
            

