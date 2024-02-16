"""

Elaborating on an example in Raymond Hettinger's presentation.

"""

from utils import *


# The following is pep8 compliant, but is it good code?


ts('obama', 20, False, True)


# Changing the name, already much clearer, but what the arguments do
# (except for the first one) is not clear.

twitter_search('obama', 20, False, True)


# Using named arguments to make the code clearer and more robust.

twitter_search('obama', numtweets=20, retweets=False, encoding='utf8')


# Let's go to the function definition. Even with bad names, it usually does give
# away what it does, but it may take some effort and require to poke around in the
# body of the code. In the function definition you should pick your names well and
# in many cases use type hints.

def twitter_search(term: str, numtweets: int, retweets: bool = True, encoding: str = 'utf8'):
    pass


# The definition above does gives you what you need to know in most cases. It does
# violate pep8 though, unless you are not stuck up on a line length of 79 but use
# ninety-ish instead. Nevertheless, when the line gets really long you would start
# using more lines

def twitter_search(
        term: str,
        numtweets: int = 10,
        retweets: bool = True,
        unicode: bool = True):
    print(term, numtweets, retweets, unicode)
    #term + 'postfix'


# Of course, Python still allows the following and you won't know it is bad
# untill you get a runtime error.

twitter_search(20, retweets='10')
