# Day 3: Pattern Printing with Single Loops & String Formatting (ASCII Christmas Tree Generator)
height = 5 # Set row in height

for i in range(1, height + 1): # Loop in row starting at 1 to 5 (range stops before 6)
    spaces = " " * (height - i) # Calculate leading spaces starting at 4 on row 1 and decrease down to 0 on row 5
    stars = "*" * (2 * i - 1) # Calculate star by using odd number math (2 * i - 1), (1, 3, 5, 7, 9)
    print(spaces + stars) # Print spaces First then p`ush the starts towards the centre, then the stars

print(" " * (height - 1) + "|")  # Print 4 spaces then "|" so the Christmas tree can have a trunk right at the centre directly under the top star

