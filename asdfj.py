i = 0
while i < 1000:
    for j in range(1, i):
        if i % j == 0:
            print("keine primzahl")
            break