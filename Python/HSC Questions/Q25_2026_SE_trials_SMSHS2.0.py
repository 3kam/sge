# Table
temperatures = [
    [18, 24, 30],
    [17, 22, 19],
    [19, 25, 21],
    [16, 23, 18],
    [20, 27, 22]
]


all_temps = [temp for row in temperatures for temp in row]  # nested list lowke goated used to flatten 2D list into a 1D single list

highest = max(all_temps) # scans for the max value
lowest = min(all_temps) # scans for hte min value
average = sum(all_temps) / len(all_temps) # adds all the values and divide it by how many values are there

print("Temperature Table:") # Into statment print
print("\nHighest temperature:", highest) # Print highest
print("\nLowest temperature:", lowest) # Print lowest 
print("\nAverage temperature:", round(average, 2)) # Print average by rounding of 2 d.p.