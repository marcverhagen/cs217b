# context managers

from utils import File

def example1():
    # every time you opened a file like this you have used a context managers
    print('>>> example1()')
    with open('errors.py') as fh:
        print(f'Line 1 of errors.py: {fh.readlines()[0]}')

def example2():
    # This is pretty much the same as example1().
    print('>>> example2()')
    with File('errors.py') as fh:
        print(f'Line 1 of errors.py: {fh.readlines()[0]}')

def example3():
    # this is doing much of what example2() does, but the logic that was 
    print('>>> example3()')
    try:
        fh = open('errors.py')
        print(f'Line 1 of errors.py: {fh.readlines()[0]}')
    except ZeroDivisionError as e:
        print('Ignored zero division error')
    except Exception as e:
        print('Other error, not ignoring it')
        raise e
    finally:
        fh.close()


if __name__ == '__main__':

    example1()
    example2()
    example3()
