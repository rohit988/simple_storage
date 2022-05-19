from brownie import crowdfunding, accounts


def test_retrieve():
    account = accounts[0]
    simple_storages = crowdfunding.deploy({"from": account})

    starting = simple_storages.empty()
    print(starting)
    expected = 0
    assert starting == expected


def test_other():
    account = accounts[0]
    simple_storages = crowdfunding.deploy({"from": account})
    starting = simple_storages.non_empty(15, {"from": account})
    starting1 = simple_storages.empty()
    print(starting1)
    assert starting1 == 14
