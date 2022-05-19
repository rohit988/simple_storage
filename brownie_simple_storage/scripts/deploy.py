from brownie import accounts, crowdfunding, network
import os
from psutil import AccessDenied


def deployment():
    account = accounts_network()
    print(account)
    simple_storage = crowdfunding.deploy({"from": account})
    store = simple_storage.empty()

    print(store)
    new_store = simple_storage.non_empty(5, {"from": account})
    new_store.wait(1)
    upstore = simple_storage.empty()
    print(upstore)


def accounts_network():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(os.getenv("private_key"))


def main():
    deployment()
