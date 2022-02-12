import streamlit as st
from . import login

def render_doctor_page(username):
    st.header("Welcome doctor!")
    st.subheader("{}".format(username))

def app():
    logged_in_as_doctor,logged_in_as_patient,username = login.app()
    if logged_in_as_patient:
        st.warning("You are not logged in as doctor!")
    elif logged_in_as_doctor:
        render_doctor_page(username)
    else:
        st.warning("Please login as a doctor to access this page!")