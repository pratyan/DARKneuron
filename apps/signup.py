import streamlit as st
import numpy as np
import pandas as pd
from . import db

def app():
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    user = st.radio("Enter as a: ",("Doctor","Patient"))
    if user == "Doctor":
        specialization = st.text_input("Specialization")

    if st.button("Signup"):
        if user == "Patient":
            db.create_usertable()
            db.add_userdata(new_user,db.make_hashes(new_password),"***")
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
        if user == "Doctor":
            db.create_doctortable()
            db.add_doctordata(new_user,db.make_hashes(new_password),specialization,"***")
            st.success("You have successfully created a valid Account as a doctor")
            st.info("Go to Login Menu to login")