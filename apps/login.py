from multiapp import MultiApp
import streamlit as st
import numpy as np
import pandas as pd
from . import db


def app():
    st.image('./images/welcome_image.png')

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')
    user_type = st.sidebar.radio("Enter as a: ",("Doctor","Patient"))

    logged_in_as_patient = False
    logged_in_as_doctor = False

    if st.sidebar.checkbox("Login"):
        logged_in = True
    else:
        logged_in = False
    if user_type == "Patient":
        if logged_in:
            logged_in_as_patient = True
            db.create_usertable()
            hashed_pswd = db.make_hashes(password)

            result = db.login_user(username,db.check_hashes(password,hashed_pswd))
            if result:
                logged_in_as_patient = True
                st.success("Logged In as {}".format(username))
                # render_login_page()
            else:
                st.warning("Incorrect username/password")
    else:
        specialization = st.sidebar.text_input("Specialization")
        if logged_in:
            logged_in_as_doctor = True
            db.create_doctortable()
            hashed_pswd = db.make_hashes(password)

            result = db.login_doctor(username,db.check_hashes(password,hashed_pswd),specialization)
            if result:
                logged_in_as_doctor = True
                st.success("Logged In as {}".format(username))
                # render_login_page()
            else:
                st.warning("Incorrect username/password")

    return logged_in_as_doctor,logged_in_as_patient,username