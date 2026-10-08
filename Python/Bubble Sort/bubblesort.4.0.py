import time
import os

def display_pengiuns(v):  # Keeping your spelling here
    os.system('cls' if os.name == 'nt' else 'clear')
    max_height = max(v)
    print("Sorting the penguins from smallest to largest:\n")
    for h in range(max_height, 0, -1):
        line = ""  # FIXED: Changed '-' to '='
        for penguin_height in v:
            if penguin_height >= h:
                line += "  🐧  "
            else:
                line += "      "
        print(line)
    print("".join([f"  [{x}]  " for x in v]))
    print("\n" + "=" * (len(v) * 6))

v = [7, 4, 2, 1, 8, 3, 6, 5]
n = len(v)

display_pengiuns(v)  # FIXED: Matched the spelling of your function
time.sleep(1.5)

for i in range(n - 1):
    ok = True
    for j in range(n - 1 - i):
        if v[j] > v[j+1]:
            v[j], v[j+1] = v[j+1], v[j]
            ok = False  # Note: Indenting this inside the 'if' makes it run smoother!
            display_pengiuns(v)
            time.sleep(0.6)
    if ok:
        break

print("\nAll penguins are perfectly sorted!!!")
