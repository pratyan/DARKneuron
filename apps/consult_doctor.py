import streamlit as st
from . import login,db
import pandas as pd
from web3 import Web3

#for connecting to Ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'

doctor_address = '0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'
doctor_key = '0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d'

#contract object
contract_address = '0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab'
contract_abi = [{'inputs': [], 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'inputs': [], 'name': 'breakAccess', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_doctor', 'type': 'address'}], 'name': 'breakAccessByPatient', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_newHead', 'type': 'address'}], 'name': 'changeHead', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '_doctor', 'type': 'address'}], 'name': 'giveAccess', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'address', 'name': '', 'type': 'address'}, {'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'name': 'ledger', 'outputs': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'address', 'name': 'patientAddress', 'type': 'address'}, {'internalType': 'string', 'name': 'prediction', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'recieveByDoctor', 'outputs': [{'components': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'address', 'name': 'patientAddress', 'type': 'address'}, {'internalType': 'string[]', 'name': 'symptoms', 'type': 'string[]'}, {'internalType': 'string', 'name': 'prediction', 'type': 'string'}], 'internalType': 'struct Patient_Data.Report[]', 'name': '', 'type': 'tuple[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'recieveByPatient', 'outputs': [{'components': [{'internalType': 'string', 'name': 'name', 'type': 'string'}, {'internalType': 'address', 'name': 'patientAddress', 'type': 'address'}, {'internalType': 'string[]', 'name': 'symptoms', 'type': 'string[]'}, {'internalType': 'string', 'name': 'prediction', 'type': 'string'}], 'internalType': 'struct Patient_Data.Report[]', 'name': '', 'type': 'tuple[]'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [{'internalType': 'string', 'name': '_name', 'type': 'string'}, {'internalType': 'string[]', 'name': '_symptoms', 'type': 'string[]'}, {'internalType': 'string', 'name': '_pridiction', 'type': 'string'}], 'name': 'upload', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}]

contract = w3.eth.contract(address = contract_address, abi=contract_abi) # contract object after the transaction

def app():
    logged_in_as_doctor,logged_in_as_patient,username = login.app()
    book = False
    if logged_in_as_patient:
        col1,col2,col3 = st.columns(3)
        with col1:
            pass
        with col2:
            book = st.checkbox("Book an appointment")
        with col3:
            pass
    elif logged_in_as_doctor:
        st.warning("You are not logged in as patient!")
    else:
        st.warning("Please login as a patient to access this page!")

    if book:
        names = []
        specs = []
        data = db.view_all_doctors()
        for doctor in data:
            names.append(doctor[0])
            specs.append(doctor[2])

        df = pd.DataFrame(data = {"Name" : names, "Specialization" : specs})
        st.table(df)
        st.subheader("Check the box next to desired doctor name")
        index = -1
        for i in range(0,len(names)):
            flag = st.checkbox(df['Name'][i])
            if flag:
                index = i

        if index!=-1:
            doctorname = df['Name'][index]
            db.update_userdoctor(doctorname,username)
            db.update_doctorpatient(username,doctorname)
            st.header("Appointment booked with {}".format(doctorname))

            #Access button
            if st.button("Give Access To Your Reports"):
                nonce = w3.eth.getTransactionCount(my_address)-1 #Basically the number of transaction by the curent accnt

                #1
                store_transaction = contract.functions.giveAccess(my_address).buildTransaction(
                        {"chainId":chain_id, "from":my_address, "nonce":nonce+1}
                    ) #"nonce" =+1 since after the declaration of the variable we have done one transaction
                #2
                signed_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
                #3
                send_store_transaction = w3.eth.sendRawTransaction(signed_store_transaction.rawTransaction)
                # wait for the complition of the transaction
                transaction_receipt = w3.eth.waitForTransactionReceipt(send_store_transaction)

                st.success('Access Granted !')
