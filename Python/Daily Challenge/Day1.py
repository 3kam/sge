# Day 1: Control Structures & Modulo Operations
num = int(input("Enter an integar: "))

# Check if integar if divisible by both 3 and 5
if num % 3 == 0 and num % 5 == 0:
    print("FizzBuzz")
# Check if integar is only divisible by 3
elif num % 3 == 0:
    print("Fizz")
# Check if integar is only divisible by 5
elif num % 5 == 0:
    print("Buzz")
# Print integar in an string format if the integar is neither divisible by 3 or 5
else:
    print(str(num))