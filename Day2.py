# Day 2: Data Validation & Exception Handling
def get_valid_age():
    while True:
        try:
            age = int(input("Enter a valid age (0-120): "))
            if 0 <= age <= 120:
                return age
            else:
                print("Error: Age is not valid.")
        except ValueError:
            print("Error: Please enter a whole digit value.")

user_age = get_valid_age()
unit = "year old" if user_age == 1 else "years old"
print(f"Validated age entered: {user_age} {unit}")