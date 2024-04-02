
class Person:

    instances = 0

    def __new__(cls, name):
        if Person.instances >= 2:
            raise Exception("too many instances")
        Person.instances += 1
        return super().__new__(cls)

    def __init__(self, name):
        self.name = name


for name in ('sue', 'joe', 'kim'):
    try:
        person = Person(name)
        print(f"<Person {person.name}>")
    except Exception as e:
        print(f'Could not create {name}: {e}')


