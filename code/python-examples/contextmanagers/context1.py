# Context managers

from utils import File

def example1():
    # Every time you opened a file like this you have used a context managers
    print('\n>>> example1()')
    with open('example.txt') as fh:
        print(f'Line 1 of example.txt: {fh.readlines()[0]}', end='')
    print('=== done')

def example2():
    # This is pretty much the same as example1().
    print('\n>>> example2()')
    with File('example.txt') as fh:
        print(f'Line 1 of example.txt: {fh.readlines()[0]}', end='')
    print('=== done')

def example3():
    # This is doing much of what example2() does, but the logic of the context
    # manager is made explicit. 
    print('\n>>> example3()')
    try:
        print('--- entering...')
        fh = open('example.txt')
        # 1/0
        # raise Exception
        print(f'Line 1 of example.txt: {fh.readlines()[0]}', end='')
    except ZeroDivisionError as e:
        print('--- Ignored zero division error')
    except Exception as e:
        print('--- Other error, not ignoring it')
        raise e
    finally:
        print(f'--- closing example.txt')
        fh.close()
    print('=== done')


if __name__ == '__main__':

    example1()
    example2()
    example3()
