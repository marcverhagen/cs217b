
ACCOUNT_ID = 0

class Account(object):

    def __init__(self, id): 
        self.id = id

    def __str__(self):  
        return "<Account id=%d>" % self.id


def create_account():
    global ACCOUNT_ID 
    ACCOUNT_ID += 1
    return Account(ACCOUNT_ID)

   
print(create_account())
print(create_account())
