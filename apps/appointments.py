import streamlit as st
from . import login,db

def app():
    logged_in_as_doctor,logged_in_as_patient,username = login.app()
    if logged_in_as_patient:
        doctorname = db.get_doctorname(username)
        if doctorname=="***":
            st.header("You have no appointments yet")
        else:
            st.header("You have an appointment with Dr. {}".format(doctorname))
    elif logged_in_as_doctor:
        st.warning("You are not logged in as patient!")
    else:
        st.warning("Please login as a patient to access this page!")