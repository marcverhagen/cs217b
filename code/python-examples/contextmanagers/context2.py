# Context managers

from utils import File


def example4():
    # We introduce an error in the body, which will be caught
    print('\n>>> example4()')
    with File('example.txt') as fh:
        1/0
    print('=== done')

def example5():
    # Other exceptions are not ignored by the context manager
    print('\n>>> example5()')
    with File('example.txt') as fh:
        open('xxx')
    print('=== done')


if __name__ == '__main__':

    example4()
    example5()
