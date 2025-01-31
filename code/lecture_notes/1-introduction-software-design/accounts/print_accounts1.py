from account_utils import *

def print_accounts():
    accounts = collect_accounts() 
    accounts = reduce_accounts(accounts)
    print_to_stdout(accounts)

def print_accounts_to_file ():
    accounts = collect_accounts() 
    accounts = reduce_accounts(accounts)
    print_to_file(accounts)