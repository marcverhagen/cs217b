
def example3():
    print('\n>>> divide(2, 1)')
    divide(2, 1)
    print('\n>>> divide(2, 0)')
    divide(2, 0)
    print('\n>>> divide("2", "1")')
    divide("2", "1")
    print()

def divide(x, y):
    # https://docs.python.org/3/tutorial/errors.html#defining-clean-up-actions
    try:
        result = x / y
    except ZeroDivisionError:
        print("division by zero!")
    else:
        print("result is", result)
    finally:
        print("executing finally clause")

def example4():
    print('\n>>> example4()')
    try:
        fh = open('errors.py')
        #raise Exception
        1/0
    except ZeroDivisionError as e:
        print(type(e).__name__, e)
    finally:
        print('closing file')
        fh.close()
    print('file is closed:', fh.closed)


if __name__ == '__main__':

    example4()

