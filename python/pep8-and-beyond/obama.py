"""

Elaborating on an example in Raymond Hettinger's presentation.

Note that if you run this you will get errors because of missing function definitions.

"""

# The following is pep8 compliant, but is it good code?

ts('obama', 20, False, True)


# Changing the name from obama1.py, already much clearer, but what the arguments do
# (except for the first one) is not clear.

twitter_search('obama', 20, False, True)


# Using named arguments to make the code even clearer and you can make changes with
# much more confidence.

twitter_search('obama', numtweets=20, retweets=False, unicode=True)


# Let's go to the function definition. Even with bad names, it usually does give
# away what it does, but it may take some effort and require to poke around in the
# body of the code. In the function definition you should pick your names well and
# in many cases use type hints.

def twitter_search(term: str, numtweets: int, retweets: bool = True, unicode: bool = True):
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
    pass


# Of course, Python still allows the following and you won't know it is bad
# untill you get a runtime error.

twitter_search(20, retweets=10)


# You can use mypy for type checking (if your IDE does not already do that for you).

# $ pip install mypy
# $ mypy script_name.py
