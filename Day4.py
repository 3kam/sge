# Day 4: Nested Loops & Grid Output (Multiplication Table Generator)
size = 5 # Set grid dimensions 5x5

for row in range(1, size + 1): # Outer loop control in row (1, 2, 3, 4, 5)
    for col in range(1, size + 1):  # Inner loop control the column (1, 2, 3, 4, 5)
        print(f"{row * col:3}", end="") # Multiply row and col like a table with a spacing of 3 and stay on the same line
    print() # move to next line after completing 5 in a row