# Day 2: Data Validation & Exception Handling
def get_valid_age(): # Define function of getting age input
    while True: # set an infinite loop until valid age is given
        try: # Attempt to run code that might raise an error
            age = int(input("Enter a valid age (0-120): ")) # input requesting user to enter valid age between 0-120
            if 0 <= age <= 120: # only accept these rnages
                return age
            else:
                print("Error: Age is not valid.") # Given output is out of range
        except ValueError:
            print("Error: Please enter a whole digit value.") # Given output if it is a deciaml or is an text

user_age = get_valid_age() # Call function and store validated result in user_age
unit = "year old" if user_age == 1 else "years old" # choose singular or plural unit based on age
print(f"Validated age entered: {user_age} {unit}") # final output 