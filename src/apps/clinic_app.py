import streamlit as st
import hashlib
import requests
import time
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="ClinicAI", page_icon="🤖", layout="centered")

# --- Data Structures (Refactored for Web) ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize Session State for User Database
if 'users' not in st.session_state:
    st.session_state.users = {
        "patient1": {"name": "John Doe", "pass": hash_password("pass1"), "role": "patient"},
        "davis": {"name": "Dr. Davis", "pass": hash_password("docpass1"), "role": "doctor"}
    }
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None

symptom_to_specialty = {
    "Chest Pain": "Cardiologist", "Skin Rash": "Dermatologist",
    "Fever": "General Physician", "Toothache": "Dentist",
    "Blurry Vision": "Ophthalmologist", "Back Pain": "Orthopedic",
    "Stomach Ache": "Gastroenterologist", "Persistent Cough": "Pulmonologist"
}

# --- API Logic ---
def find_real_doctors(city, specialty):
    headers = {'User-Agent': 'ClinicAI_App_mddilshad@gmail.com'}
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    
    try:
        geo_res = requests.get(geo_url, headers=headers).json()
        if not geo_res: return []
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']

        overpass_url = "https://overpass.kumi.systems/api/interpreter"
        overpass_query = f"""[out:json][timeout:25];node["amenity"~"doctors|clinic"](around:10000,{lat},{lon});out body;"""
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers)
        
        if response.status_code == 200:
            return [{"Name": e['tags'].get('name', 'Local Clinic'), 
                     "Address": e['tags'].get('addr:street', 'Nearby Area')} 
                    for e in response.json().get('elements', [])]
        return []
    except:
        return []

# --- UI Components ---
def login_page():
    st.title("🏥 ClinicAI")
    st.subheader("Login or Register")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            if u in st.session_state.users and st.session_state.users[u]['pass'] == hash_password(p):
                st.session_state.logged_in_user = st.session_state.users[u]
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type="password")
        new_name = st.text_input("Full Name")
        role = st.selectbox("Role", ["patient", "doctor"])
        if st.button("Register"):
            st.session_state.users[new_u] = {"name": new_name, "pass": hash_password(new_p), "role": role}
            st.success("Account created! Go to Login tab.")

def patient_portal():
    user = st.session_state.logged_in_user
    st.title(f"👋 Welcome, {user['name']}")
    
    symptom = st.selectbox("What is your primary symptom?", list(symptom_to_specialty.keys()))
    city = st.text_input("Enter your city (e.g., Patna, Bengaluru)")
    
    if st.button("Find Help"):
        with st.spinner("Analyzing and searching..."):
            specialty = symptom_to_specialty[symptom]
            st.info(f"Guidance: Based on your symptom, you should see a **{specialty}**.")
            
            docs = find_real_doctors(city, specialty)
            if docs:
                st.success(f"Found {len(docs)} clinics near {city}!")
                st.table(pd.DataFrame(docs).head(10))
            else:
                st.warning("No live records found. Try a bigger city nearby.")

def doctor_portal():
    st.title("🩺 Doctor Dashboard")
    st.write("Current Patient Activity Logs")
    # In a real app, you'd pull from a DB. Here we simulate:
    st.info("Log Viewer Feature (Backend Connected)")
    if st.button("Refresh Logs"):
        st.write("No new logs in this session.")

# --- Main App Logic ---
if st.session_state.logged_in_user:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()
    
    if st.session_state.logged_in_user['role'] == 'doctor':
        doctor_dashboard = doctor_portal()
    else:
        patient_portal()
else:
    login_page()