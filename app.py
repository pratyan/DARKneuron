import streamlit as st
from multiapp import MultiApp
from apps import home,signup,login,self_diagnosis,consult_doctor,doctor_interface,appointments,patients


app = MultiApp()
title = '<h1 style="text-align:center">CLICK-A-CLINIC</h1>'
st.markdown(title,unsafe_allow_html=True)
m = '<h3 style="text-align:center">By DARKneuron</h3>'
st.markdown(m,unsafe_allow_html=True)

app.add_app("Home", home.app)
app.add_app("Login", login.app)
app.add_app("signup", signup.app)
app.add_app("SELF DIAGNOSIS", self_diagnosis.app)
app.add_app("Consult a doctor", consult_doctor.app)
app.add_app("Doctor's interface",doctor_interface.app)
app.add_app("My appointments",appointments.app)
app.add_app("My patients",patients.app)

app.run()