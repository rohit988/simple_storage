from asyncore import read
from brownie import crowdfunding, network, accounts


def read_function():
    simple_storage = crowdfunding[1]
    print(simple_storage.empty())


def main():
    read_function()
