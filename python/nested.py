def outer_function():
    message = 'outer peace'

    def inner_function():
        nonlocal message
        message += ' inner peace'
        print(message)

    print(message)
    inner_function()
    print(message)

outer_function()
outer_function()
