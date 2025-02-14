# Context managers

from utils import File


def example6():
    # This one will crash the script in any case since the error doesn't
    # occur in the body of the context
    print('\n>>> example6()')
    with File('xxx') as fh:
        print('Howdy')
    print('=== done')


if __name__ == '__main__':

    example6()
