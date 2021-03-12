import itertools
test = [0,1,2,3,4,5]
test = iter(test)

count = 0

while count < 3:
    x = tuple(itertools.islice(test, 1))
    print(x)
    count += 1
