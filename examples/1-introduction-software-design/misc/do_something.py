def do_something(list):
    count = 0
    for thing in list:
        # increment the count
        count += 1
        thing.id = count


def add_identifier(bank_accounts: list):
    """Add unique identifiers to bank 
    bank_accounts. Identifiers start at 1."""
    for n, account in enumerate(bank_accounts):
        account_id = n + 1
        account.identifier = account_id

