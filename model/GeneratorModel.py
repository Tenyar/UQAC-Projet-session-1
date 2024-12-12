#   GeneratorModel Class (concern generating a random password secured for the client for any site/app)
import string
import random
import math
from collections import Counter

# Importing DAO constants
from utility.ConstantsUtility import (
    DEFAULT_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, MAX_ENTROPY
)

class GeneratorModel:
    def __init__(self):
        self.entropy = None


    def get_entropy(self):
        return self.entropy
    

    def generate_password(self, gen_values):
        print('*******  Generating a new password  *******')
        params = {
        "service_name" : gen_values["service_name"],
        "password_length" : gen_values["password_length"],   # 8 - 128 characters
        "lowercase_alphabet" :  gen_values["lowercase_alphabet"],   # a-z
        "uppercase_alphabet" :  gen_values["uppercase_alphabet"],   # A-Z
        "numbers" :  gen_values["numbers"],  #0-9
        "special_chars" :  gen_values["special_chars"], # @!#$(). . .
        "min_numbers" :  gen_values["min_numbers"],  # minimum of numbers present in the password
        "min_special_chars" :  gen_values["min_special_chars"]  # minimum of specials characters present in the password
        }
        #   Parameters for generating a passwords
        lowercase_pool = None   #   Define a lowercase character pool
        uppercase_pool = None   #   Define an upper character pool
        numbers_pool  = None    #   Define a pool of number
        specials_pool = None    #   Define a pool of number
        all_chars = None    #   Create a combined pool of characters based on enabled options
        password = None     #   Where all the characters/numbers/specials are stored

        #   Verify input (at least one option must be true)
        params = self.verify_password(params)
        #   Display password settings
        print('--------------------------')
        for key, value in params.items():
                print(f"value {key} : {value}")
        print('--------------------------')

        print("Params after verify_password:", params)

        #   Generate a password with the parameters
        lowercase_pool = string.ascii_lowercase if params["lowercase_alphabet"] == True else ""
        uppercase_pool = string.ascii_uppercase if params["uppercase_alphabet"] == True else ""
        numbers_pool  = string.digits if params["numbers"] == True else ""
        specials_pool = "!@#$%^&*()_+-=[]{}|;:',.<>?/" if params["special_chars"] == True else ""
        
        all_chars = lowercase_pool + uppercase_pool
        password = []

        #   Ensure minimum numbers and special characters
        if numbers_pool:
            chosen_numbers = random.choices(numbers_pool, k=params["min_numbers"])
            password.extend(chosen_numbers)
            print("Chosen numbers:", chosen_numbers)

        if specials_pool:
            chosen_specials = random.choices(specials_pool, k=params["min_special_chars"])
            password.extend(chosen_specials)
            print("Chosen specials:", chosen_specials)

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

        self.calculate_combined_entropy(final_password)    
        return final_password
    

    def calculate_password_entropy(self, password):
        #   Define the character pools
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        specials = '!@#$%^&*()-_=+[]{}|;:,.<>?/`~'

        char_sets = []
        if any(c in lowercase for c in password):
            char_sets.append(lowercase)
        if any(c in uppercase for c in password):
            char_sets.append(uppercase)
        if any(c in digits for c in password):
            char_sets.append(digits)
        if any(c in specials for c in password):
            char_sets.append(specials)

        # Combine the used character sets
        all_chars = ''.join(char_sets)
        print("\n\n  ALLLL CHARSSSSSSS :", all_chars)
        # Calculate the number of possible characters
        num_chars = len(all_chars)

        # Calculate the entropy
        self.entropy = math.log2(num_chars ** len(password))


    def calculate_shannon_entropy(self, password):
        #   Calculate the frequency of each character in the password
        char_counts = Counter(password)
        total_chars = len(password)

        #   Calculate the Shannon entropy
        entropy = 0
        for count in char_counts.values():
            p = count / total_chars
            entropy -= p * math.log2(p)

        #   Scale the entropy by the total number of characters
        entropy *= total_chars

        return entropy


    def calculate_character_set_entropy(self, password):
        #   Define the character pools
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        specials = '!@#$%^&*()-_=+[]{}|;:,.<>?/`~'

        #   Determine which character pools are used in the password
        char_sets = []
        if any(c in lowercase for c in password):
            char_sets.append(lowercase)
        if any(c in uppercase for c in password):
            char_sets.append(uppercase)
        if any(c in digits for c in password):
            char_sets.append(digits)
        if any(c in specials for c in password):
            char_sets.append(specials)

        #   Combine the used character sets
        all_chars = ''.join(char_sets)
        #   Calculate the number of possible characters
        num_chars = len(all_chars)
        #   Calculate the entropy
        entropy = math.log2(num_chars ** len(password))

        return entropy


    def calculate_combined_entropy(self, password):
        shannon_entropy = self.calculate_shannon_entropy(password)
        character_set_entropy = self.calculate_character_set_entropy(password)
        #   Combine the entropies
        combined_entropy = (shannon_entropy + character_set_entropy) / 2
        #   Round the entropy to the nearest integer for human readability
        combined_entropy = round(combined_entropy)
        self.entropy = combined_entropy


    def verify_password(self, params: dict):
    #   Validate all hash parameters at once.
        validated_params = params
        #   Check if no options has been set to true (means that nothing can be created), then put a-z at least to true
        if params["uppercase_alphabet"] == False & params["numbers"] == False & params["special_chars"] == False:
            params["lowercase_alphabet"] = True

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
            validated_params["min_special_chars"] = max(0, min(int(params["min_special_chars"]), validated_params["password_length"]))
        else:
            validated_params["min_special_chars"] = params["min_special_chars"]


        #   adjust the password if there's more numbers and specials characters than the password length
        # ? Additionner les valeurs et mitigué ensuite
        added_options_numbers = validated_params["min_numbers"] + validated_params["min_special_chars"]
        if added_options_numbers > validated_params["password_length"]:
            scale_factor  = (validated_params["password_length"] / added_options_numbers)
            validated_params["min_numbers"] = validated_params["min_numbers"] * scale_factor
            validated_params["min_special_chars"] = validated_params["min_special_chars"] * scale_factor
            rounded_value_1 = round(validated_params["min_numbers"] * scale_factor)
            rounded_value_2 = round(validated_params["min_special_chars"] * scale_factor)

            round_sum_params = rounded_value_1 + rounded_value_2
            print("should be max_length : ", round_sum_params)

            #   More error gandling if one numbers is off by one
            if round_sum_params < validated_params["password_length"]:
                #   Add 1 to the value with the higher decimal component
                if (validated_params["min_numbers"] - rounded_value_1) > (validated_params["min_special_chars"] - rounded_value_2):
                    rounded_value_1 += 1
                else:
                    rounded_value_2 += 1
            elif round_sum_params > validated_params["password_length"]:
                # Subtract 1 from the value with the higher decimal component
                if (validated_params["min_numbers"] - rounded_value_1) > (validated_params["min_special_chars"] - rounded_value_2):
                    rounded_value_1 -= 1
                else:
                    rounded_value_2 -= 1

            validated_params["min_numbers"] = rounded_value_1
            validated_params["min_special_chars"] = rounded_value_2
        return validated_params