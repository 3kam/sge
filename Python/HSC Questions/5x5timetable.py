# List of subjcets
subjects = ["English", "Software", "Physics", "Economics", "Maths"]
# List of school days
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Loop through each school day
for day in days:
    # Display the current day
    print(day) 

    # Loop through the five periods
    for i in range(5):
        # Display the period number and subject
        print("P" + str(i + 1) + ":", subjects[i])
    # Add blank line between each day
    print()
    # Move the last subject to the first position of the next day
    subjects.insert(0, subjects.pop())

