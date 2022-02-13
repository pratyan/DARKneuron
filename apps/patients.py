import streamlit as st
from . import login,db
from web3 import Web3

#for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'

doctor_address = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
doctor_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'
nonce = w3.eth.getTransactionCount(my_address) #Basically the number of transaction by the curent accnt

#contract object
contract_address = '0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab'
contract_abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'breakAccess', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_doctor', 'type': 'address'}], 'name': 'breakAccessByPatient', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_newHead', 'type': 'address'}], 'name': 'changeHead', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_doctor', 'type': 'address'}], 'name': 'giveAccess', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'ledger', 'outputs': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'address', 'name': 'patientAddress', 'type': 'address'}, {'internalType': 'string', 'name': 'prediction', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'recieveByDoctor', 'outputs': [{'components': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'address', 'name': 'patientAddress', 'type': 'address'}, {'internalType': 'string[]', 'name': 'symptoms', 'type': 'string[]'}, {'internalType': 'string', 'name': 'prediction', 'type': 'string'}], 'internalType': 'struct Patient_Data.Report[]', 'name': '', 'type': 'tuple[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'recieveByPatient', 'outputs': [{'components': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'address', 'name': 'patientAddress', 'type': 'address'}, {'internalType': 'string[]', 'name': 'symptoms', 'type': 'string[]'}, {'internalType': 'string', 'name': 'prediction', 'type': 'string'}], 'internalType': 'struct Patient_Data.Report[]', 'name': '', 'type': 'tuple[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': '_name', 'type': 'string'}, {'internalType': 'string[]', 'name': '_symptoms', 'type': 'string[]'}, {'internalType': 'string', 'name': '_pridiction', 'type': 'string'}], 'name': 'upload', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}]

contract = w3.eth.contract(address = contract_address, abi=contract_abi) # contract object after the transaction


def app():
    logged_in_as_doctor,logged_in_as_patient,username = login.app()
    pending=False
    if logged_in_as_doctor:
        patientname = db.get_patientname(username)
        if patientname=="***":
            st.header("You have no appointments yet")
        else:
            pending=True
            st.header("You have an appointment with {}".format(patientname))
            
    elif logged_in_as_doctor:
        st.warning("You are not logged in as a doctor!")
    else:
        st.warning("Please login as a doctor to access this page!")

    if pending:
        st.subheader("Schedule a meeting here..")
        date = st.text_input("Date:")
        time = st.text_input("Time:")
        if st.button("Schedule"):
            db.create_appointmenttable()
            db.add_appointment(username,patientname,date,time)
            st.subheader("Appointment scheduled with {} at date: {} ,time: {}".format(patientname,date,time))

    if st.button("Get Patient's Reports"):
        try:
            st.write(contract.functions.recieveByDoctor().call())
        except:
            st.warning("Not authorized !")


