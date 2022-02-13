import streamlit as st
from . import login,db

def app():
    date = ""
    time =""
    logged_in_as_doctor,logged_in_as_patient,username = login.app()
    if logged_in_as_patient:
        doctorname = db.get_doctorname(username)
        if doctorname=="***":
            st.header("You have no appointments yet")
        else:
            st.header("You have an appointment with Dr. {}".format(doctorname))
            date,time = db.get_appointment_patient(username)
            st.subheader("Date : {}".format(date))
            st.subheader("Time : {}".format(time))
    elif logged_in_as_doctor:
        st.warning("You are not logged in as patient!")
    else:
        st.warning("Please login as a patient to access this page!")
