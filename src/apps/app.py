import streamlit as st
import pandas as pd
import requests
import json
import time
import google.generativeai as genai

# Architect's Note: Never hardcode your API Key in a public GitHub repo.
# For local testing, you can paste it here. For production, use st.secrets.
genai.configure(api_key="GOOGLE_GEMINI_API_KEY")

# Define the "System Instruction" to guide the AI's behavior
system_instruction = """
You are a medical triage assistant for ClinicAI. 
Your goal is to analyze user symptoms and suggest a medical specialty (e.g., Cardiologist, Dentist).
1. Always include a disclaimer: "I am an AI, not a doctor. In an emergency, call 102."
2. Be concise and professional.
3. If symptoms sound life-threatening, tell them to stop typing and go to the ER immediately.
"""

# Use the current state-of-the-art Flash model
model = genai.GenerativeModel(
    model_name="gemini-3-flash", # This is the current professional standard
    system_instruction=system_instruction
)

# --- 1. SYSTEM ARCHITECTURE & STATE ---
# This ensures the app remembers who is logged in
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""

# --- 2. BACKEND LOGIC (The "Engine") ---

def find_real_doctors(city, specialty):
    """Uses OpenStreetMap (Nominatim + Overpass) for real-world data."""
    headers = {'User-Agent': 'ClinicAI_Founder_App_Contact_mddilshad@gmail.com'}
    try:
        # Step A: Get City Coordinates
        geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        geo_res = requests.get(geo_url, headers=headers).json()
        if not geo_res: return []
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']

        # Step B: Overpass API for Doctors/Clinics
        overpass_url = "https://overpass.kumi.systems/api/interpreter"
        query = f"""[out:json][timeout:25];
                   node["amenity"~"doctors|clinic"](around:5000,{lat},{lon});
                   out body;"""
        response = requests.get(overpass_url, params={'data': query}, headers=headers)
        if response.status_code == 200:
            elements = response.json().get('elements', [])
            return [{"name": e.get('tags', {}).get('name', 'Local Clinic'), 
                     "addr": e.get('tags', {}).get('addr:street', 'Nearby Area')} for e in elements]
        return []
    except:
        return []

# --- 3. UI COMPONENTS (The "Front-End") ---

def login_page():
    st.title("🏥 ClinicAI: Healthcare OS")
    st.subheader("Founder's Edition | Self-Made Architecture")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.selectbox("I am a...", ["Patient", "Doctor"])
    with col2:
        name = st.text_input("Full Name")
    
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    
    if st.button("Access Dashboard"):
        if user and pwd: # Simplified for your current lab phase
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.user_name = name if name else user
            st.rerun()

def patient_dashboard():
    st.sidebar.title(f"Welcome, {st.session_state.user_name}")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["AI Symptom Tracker", "Health Calculators", "Maintenance Guide"])

    with tab1:
        st.header("AI Symptom Analysis")
        symptom_input = st.text_area("Describe your symptoms in detail (e.g., 'I have a sharp pain in my chest and cold sweats'):")
        city = st.text_input("Enter your city for nearby clinic search:")

        if st.button("Run AI Analysis"):
            if symptom_input and city:
                with st.spinner("AI is analyzing symptoms..."):
                    # The AI "Brain" works here
                    response = model.generate_content(symptom_input)
                    st.markdown("### AI Assessment")
                    st.write(response.text)
                    
                    st.divider()
                    
                    # The Search "Body" works here
                    st.subheader(f"Specialists found in {city}")
                    doctors = find_real_doctors(city, "Clinic")
                    if doctors:
                        for d in doctors[:5]:
                            st.write(f"👨‍⚕️ **{d['name']}** | 📍 {d['addr']}")
                    else:
                        st.info("No clinics found in OpenStreetMap data for this specific area.")

    with tab2:
        st.header("Quick Health Tools")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("BMI Calculator")
            w = st.number_input("Weight (kg)", 30, 200, 70)
            h = st.number_input("Height (cm)", 100, 250, 170)
            bmi = round(w / (h/100)**2, 2)
            st.metric("Your BMI", bmi)
            if bmi < 18.5: st.info("Underweight")
            elif 18.5 <= bmi < 25: st.success("Healthy Weight")
            else: st.warning("Overweight/Obesity focus recommended")
            
        with c2:
            st.subheader("🚨 Emergency")
            st.error("**Ambulance: 102**")
            st.error("**National Emergency: 112**")

    with tab3:
        st.header("Daily Health Maintenance")
        focus = st.select_slider("Select Health Focus", 
                                options=["General", "Diabetic", "Low BP", "High BP", "Obesity"])
        
        advice = {
            "General": "Sleep 8 hours, drink 3L water, and walk 5k steps.",
            "Diabetic": "Focus on low-GI foods (oats, leafy greens). Monitor glucose levels 2h after meals.",
            "Low BP": "Increase fluid/salt intake slightly. Avoid sudden standing movements.",
            "High BP": "Reduce sodium (salt). Focus on Potassium-rich foods like bananas/spinach.",
            "Obesity": "High-intensity intervals (HIIT). 5am Jogging. Calorie deficit is mandatory."
        }
        st.info(f"**Action Plan for {focus}:** \n\n {advice[focus]}")

def doctor_dashboard():
    st.sidebar.title(f"Dr. {st.session_state.user_name}")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Clinical Administration")
    specialty = st.text_input("Confirm your Professional Specialty:")
    
    st.subheader("Patient Queue & Case Logs")
    # This simulates reading from your patient_history.txt
    st.info("Searching for recent patient entries in your district...")
    st.table({"Time": ["14:20", "15:10"], "Patient": ["John Doe", "Amit Kumar"], "Symptom": ["Fever", "Chest Pain"]})

# --- 4. MAIN EXECUTION ---
if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == "Patient":
        patient_dashboard()
    else:
        doctor_dashboard()


