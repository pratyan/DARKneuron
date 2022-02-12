from solcx import compile_standard, install_solc
import json
from web3 import Web3

# read the solidity file
with open("./Click_A_Clinic.sol", "r") as file:
	Click_A_Clinic_file = file.read()
	# print(simple_storage_file)


# installing solc_version  "0.8.0"
install_solc("0.8.0")

# complie our solidity
compiled_sol = compile_standard(
	{
		"language": "Solidity",
		"sources": {"Click_A_Clinic.sol": {"content": Click_A_Clinic_file}},
		"settings": {
			"outputSelection": {
				"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
			}
		},
	},
	solc_version="0.8.0",
)

# print(compiled_sol)

#now gonna dumb the complied code to a json file
with open("compiled_code.json", "w") as file:
	json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["Click_A_Clinic.sol"]["Patient_Data"]["evm"][
	"bytecode"
]["object"]


#get abi
abi = compiled_sol["contracts"]["Click_A_Clinic.sol"]["Patient_Data"]["abi"]

# print(bytecode) 

#for connection to genache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"


#create the contract object
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
#get the nonce
nonce = w3.eth.getTransactionCount(my_address)
#print(nonce)


##1.Build a transaction
##2.Sign a transaction
##3.Send a transaction

#1
transaction = contract.constructor().buildTransaction(
		{"chainId":chain_id, "from":my_address, "nonce":nonce}
)
#2
signed_transaction = w3.eth.account.sign_transaction(transaction,private_key=private_key)
#3
print("Deploying contract..")
transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
# to wait until the transaction happens
transaction_receipt = w3.eth.waitForTransactionReceipt(transaction_hash) #And, this variable stores the contract address
print("Deplyed!")


print(transaction_receipt.contractAddress)
print(abi)
