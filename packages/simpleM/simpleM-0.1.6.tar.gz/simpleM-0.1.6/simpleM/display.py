def f():
    print("hello, world")
    with open('.simpleM/b.txt') as f:
        for line in f:
            print(line)