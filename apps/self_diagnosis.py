import streamlit as st
from . import login
import pickle
import pandas as pd
import numpy as np

def get_symp_hash():
    # symp_severity = pd.read_csv('C:/Users/Sharad/Desktop/files/ML/test_hack/model/Symptom-severity.csv')
    symp_severity = pd.read_csv('./model/Symptom-severity.csv')
    symp_hash = {}
    for i in range(len(symp_severity)):
        symp_hash[symp_severity['Symptom'][i]] = i

    return symp_hash

def load_model(path):
    with open(path, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model

def predict(model,data):
    symp_hash = get_symp_hash()
    d = np.zeros(shape=(1,len(symp_hash)))

    for i in range(len(data)):
        d[0][symp_hash[data[i]]] = 1		
    return (model.predict(d))	

def create_disease_hash():
    # dataset = pd.read_csv('C:/Users/Sharad/Desktop/files/ML/test_hack/model/dataset.csv')
    dataset = pd.read_csv('./model/dataset.csv')
    disease_name = [x for x in dataset['Disease'].unique()]
    disease_hash = {}
    get_disease = {}
    for x in range(len(disease_name)):
        disease_hash[disease_name[x]] = x
        get_disease[x] = disease_name[x]
    return disease_hash,get_disease


def render_diagnosis_page():
    m = '<h1 style="text-align:center">SELF DIAGNOSIS</h1>'
    st.markdown(m,unsafe_allow_html=True)
    m = '<h4 style="text-align:center">Enter your symptoms to get predictions</h4>'
    st.markdown(m,unsafe_allow_html=True)
    # st.subheader('Enter your symptoms to get predictions')    
    symptoms = ('itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_ofurine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze', 'prognosis')
    n=len(symptoms)

    # symp_hash = Model.get_symp_hash()

    checks = {symptom:False for symptom in symptoms}
    col1,col2,col3 = st.columns(3)

    with col1:
        for symptom in symptoms[:n//3]:
            checks[symptom] = st.checkbox(symptom)
    with col2:
        for symptom in symptoms[n//3:(2*n)//3]:
            checks[symptom] = st.checkbox(symptom)
    with col3:
        for symptom in symptoms[(2*n)//3:]:
            checks[symptom] = st.checkbox(symptom)

    data=[]
    for symptom in checks.keys():
        if checks[symptom]:
            data.append(symptom)
    if len(data)>0:
        disease_hash,get_disease = create_disease_hash()
        model = load_model('C:/Users/Sharad/Desktop/files/ML/test_hack/apps/rf.h5')
        st.header("You have entered the following symptoms: {}".format(",".join(data)))
        st.header("Your may have: {}".format(get_disease[predict(model,data)[0]]))
    

def app():
    logged_in_as_doctor,logged_in_as_patient,username = login.app()
    if logged_in_as_patient:
        render_diagnosis_page()
    elif logged_in_as_doctor:
        st.warning("You are not logged in as patient!")
    else:
        st.warning("Please login as a patient to access this page!")
