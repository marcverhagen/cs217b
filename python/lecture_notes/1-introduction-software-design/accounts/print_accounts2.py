from account_utils import *

def print_accounts():
    accounts = collect_and_reduce_accounts(accounts)
    print_to_stdout(accounts)

def print_accounts_to_file():
    accounts = collect_and_reduce_accounts(accounts)
    print_to_file(accounts)

def collect_and_reduce_accounts():
    accounts = collect_accounts() 
    return reduce_accounts(accounts)

