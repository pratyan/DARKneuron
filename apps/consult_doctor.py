import streamlit as st
from . import login,db
import pandas as pd

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