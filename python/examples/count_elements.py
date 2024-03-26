def total_elements_iterative(lst):
    """Return the total number of elements in a tree."""
    total = 0
    while lst:
        print('>>>', lst)
        next_element = lst.pop(0)
        #print('   ', next_element)
        if not isinstance(next_element, list):
            total += 1
        else:
            lst.extend(next_element)
    return total


tree = [
            [
                "colorless",
                "green",
                "ideas"
            ],
            [
                "sleep",
                "furiously", 
                [
                    "in",
                    [
                        "the",
                        "can"
                    ]
                ]
            ]
        ]


print(total_elements_iterative(tree))
