import itertools
x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 10]
for i in itertools.chain(x, y, iter([])):
    print(i)

print()