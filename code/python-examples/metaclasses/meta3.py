
class Distance(int):

    def __init__(self, value, unit):
        super().__init__(value)
        self.unit = unit


#d = Distance(10, 'feet')
#print(d, d*d)


class Distance(int):

    def __new__(cls, value, unit):
        instance = super().__new__(cls, value)
        instance.unit = unit
        return instance

    def X__init__(self, value, unit):
        super().__init__(value)
        self.unit = unit


d = Distance(10, 'feet')
print(d, d*d)
