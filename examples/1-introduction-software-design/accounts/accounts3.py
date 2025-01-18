class Account(object):

    identifier = 0
    def __init__(self):
        Account.identifier+=1
        self.id= Account.identifier


    def __str__(self):
          return "<Account id=%d>" % self.identifier
        

print(Account())
print(Account())