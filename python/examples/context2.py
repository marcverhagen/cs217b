# context managers

from utils import File


def example4():
    # now we introduce an error in the body, which will be caught
    print('>>> example4()')
    with File('errors.py') as fh:
        1/0

def example5():
    # other exceptions are not ignored
    print('\n>>> example5()')
    with File('errors.py') as fh:
        open('xxx')

def example6():
    # and this one will crash the script in any case since it doesn't happen
    # in the body of the context
    print('\n>>> example6()')
    with File('xxx') as fh:
        print('Howdy')


if __name__ == '__main__':

    #example4()
    #example5()
    example6()
