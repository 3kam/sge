v = [7, 4, 2, 1, 8, 3, 6, 5]
n = len(v)
print(f"Strating list: {v}\n")
for i in range(n - 1):
    ok = True
    for j in range(n - 1 - i):
        if v[j] > v[j+1]:
            v[j], v[j+1] = v[j+1], v[j]
            ok = False
            print(f"Swapped: {v[j+1] and {v[j]}} -> {v}")
    if ok:
        print("\nNo swaps made. List is sorted!")
        break
print(v)            