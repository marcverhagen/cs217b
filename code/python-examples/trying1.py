
def example1():
    print('\n>>> example1()')
    try:
        fh = open('xxx')
    except FileNotFoundError as e:
        print(e)

def example2():
    print('\n>>> example2()')
    try:
        fh = open('errors.py')
        1/0
        fh.close()
    except ZeroDivisionError as e:
        print(type(e).__name__, e)
    print('file is closed:', fh.closed)
    print()


if __name__ == '__main__':

    example1()
    example2()
