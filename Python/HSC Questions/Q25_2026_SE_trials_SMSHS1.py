temperatures = [
    [18, 24, 30],
    [17, 22, 19],
    [19, 25, 21],
    [16, 23, 18],
    [20, 27, 22]
]

highest = temperatures[0][0] # find value in rows and columns 
lowest = temperatures[0][0] # find value in rows and columns range 
total = 0 # inital total
count = 0 # Inital count

print("Temperature Table:") # Into statment print

for row in temperatures: # loop
    for value in row: # search values within a range
        # Check to find the highest value in the table
        if value > highest: # condition to find the highest value
            highest = value # output if value > highest is equal to highest = value
        # Check to find the lowest value in the table
        if value < lowest: # condition to find the lowest value
            lowest = value # output if value < lowest is equal to lowest = value
        total += value # combine all the values within the table
        count += 1 # count how many numbers are their
average = total / count # avearge

print("\nHighest temperature:", highest) # Print highest
print("\nLowest temperature:", lowest) # Print lowest 
print("\nAverage temperature:", round(average, 2)) # Print average by rounding of 2 d.p.