from os import environ
from re import S
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

install_solc("0.6.0")


# for compiling
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


compiled_Sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            },
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_Sol, file)


# whole process for deploying


# bytecode getting
bytecode = compiled_Sol["contracts"]["SimpleStorage.sol"]["crowdfunding"]["evm"][
    "bytecode"
]["object"]


# get abi
abi = compiled_Sol["contracts"]["SimpleStorage.sol"]["crowdfunding"]["abi"]


# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"


# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)


# 3 steps to deploy or change state function
# 1. build the transaction
# 2. sign the transaction
# 3. send the transaction to the blockchain


# getting nonce
nonce = w3.eth.getTransactionCount(my_address)


# build the transaction
tx_hash = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# getting private key
private_key = os.getenv("private_key")


# signing the transaction
signed_txn = w3.eth.account.sign_transaction(tx_hash, private_key=private_key)


# send transaction to blockchain
transaction = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(transaction)

# getting contract address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Initial value
print(simple_storage.functions.empty().call())
print(simple_storage.functions.non_empty(15).call())


store_transaction = simple_storage.functions.non_empty(16).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_contract = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_transaction = w3.eth.send_raw_transaction(signed_contract.rawTransaction)

print(simple_storage.functions.empty().call())
