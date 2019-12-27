import sys
x = 0
while True:

    x += 1
    if x == 1:
        try:
            me = ['i', 'k']
            print(me[3])
        except IndexError as e:
            sys.stderr.write("some shit went down")
            print('what')