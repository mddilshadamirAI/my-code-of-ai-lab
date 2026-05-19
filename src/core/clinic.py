import hashlib
import requests
import time

# --- Data Structures ---

class User:
    def __init__(self, username, password, role, full_name, address=None):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role
        self.full_name = full_name
        self.address = address

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)

# In-memory database
users = {
    "patient1": User("patient1", "pass1", "patient", "John Doe"),
    "davis": User("davis", "docpass1", "doctor", "Dr. Davis"),
}

symptom_to_specialty = {
    "Chest Pain": "Cardiologist",
    "Skin Rash": "Dermatologist",
    "Fever": "General Physician",
    "Toothache": "Dentist",
    "Blurry Vision": "Ophthalmologist",
    "Back Pain": "Orthopedic",
    "Stomach Ache": "Gastroenterologist",
    "Persistent Cough": "Pulmonologist"
}

home_treatments = {
    "Fever": "Rest and drink plenty of fluids. Consult a doctor for an accurate diagnosis",
    "Toothache": "Rinse with warm salt water and avoid cold foods. Consult a doctor for an accurate diagnosis",
    "Skin Rash": "Keep the area clean and apply a cool compress. Consult a doctor for an accurate diagnosis",
    "Back Pain": "Maintain good posture and try light stretching. Consult a doctor for an accurate diagnosis",
    "Stomach Ache": "Eat light, bland foods like toast or rice. Consult a doctor for an accurate diagnosis",
    "Persistent Cough": "Stay hydrated and try honey for throat relief. Consult a doctor for an accurate diagnosis",
    "Blurry Vision": "Rest your eyes and avoid bright screens. Consult a doctor for an accurate diagnosis",
    "Default": "Consult a doctor for an accurate diagnosis."
}

# --- Free API Engine ---
def find_real_doctors(city, specialty):
    headers = {
        'User-Agent': 'ClinicAI_Founder_App_Contact_mddilshad@gmail.com' 
    }
    
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    
    try:
        geo_res = requests.get(geo_url, headers=headers).json()
        if not geo_res:
            return []
        
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']

        overpass_url = "https://overpass.kumi.systems/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:25];
        node["amenity"~"doctors|clinic"](around:10000,{lat},{lon});
        out body;
        """
        
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            real_doctors = []
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                real_doctors.append({
                    "name": tags.get('name', f"Clinic ({specialty})"),
                    "address": tags.get('addr:street', 'Local Area'),
                    "rating": "Free Data"
                })
            return real_doctors
        return []
    except Exception:
        return []

# --- Workflows & Logging ---
def log_feedback():
    """Saves user feedback to a file."""
    feedback = input("\nWe'd love your feedback! Please share your thoughts: ")
    with open("data/feedback.txt", "a") as f:
        f.write(f"[{time.ctime()}] Feedback: {feedback}\n")
    print("Thank you for your feedback!")


def log_case(user, symptom, clinic_found):
    """Saves patient activity to a file for doctors to review."""
    with open("data/patient_history.txt", "a") as f:
        f.write(f"[{time.ctime()}] Patient: {user.full_name} | Symptom: {symptom} | City: {user.address} | Found: {clinic_found}\n")

def patient_workflow(user):
    print(f"\n--- PATIENT PORTAL | Welcome, {user.full_name} ---")
    symptoms_list = list(symptom_to_specialty.keys())
    for i, symptom in enumerate(symptoms_list, 1):
        print(f"{i}. {symptom}")
    
    try:
        choice = int(input("\nEnter the number for your symptom: "))
        if 1 <= choice <= len(symptoms_list):
            chosen_symptom = symptoms_list[choice - 1]
            specialty_needed = symptom_to_specialty[chosen_symptom]
            
            print(f"\nInitial Advice: {home_treatments.get(chosen_symptom, home_treatments['Default'])}")

            user.address = input("\nEnter your city (e.g., Patna, Jehanabad): ")
            print(f"🚀 Searching for {specialty_needed} near {user.address}...")

            doctors = find_real_doctors(user.address, specialty_needed)

            first_clinic = "None found"
            if doctors:
                print(f"\n--- Real {specialty_needed}s Found Nearby ---")
                for doc in doctors[:5]:
                    print(f"👨‍⚕️ {doc['name']} | 📍 {doc['address']}")
                first_clinic = doctors[0]['name']
            else:
                print(f"\nNo specific records for {specialty_needed} found in {user.address}.")
            
            log_case(user, chosen_symptom, first_clinic)

        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")

def doctor_dashboard(user):
    while True:
        print(f"\n--- DOCTOR PORTAL | Dr. {user.full_name} ---")
        print("1. View Patient Case Logs")
        print("2. Logout")
        
        choice = input("\nSelection: ")
        if choice == "1":
            try:
                with open("data/patient_history.txt", "r") as f:
                    print("\n--- Clinical Patient Logs ---")
                    print(f.read())
            except FileNotFoundError:
                print("\n[!] No patient records found yet.")
        elif choice == "2":
            break

# --- Main Application ---

if __name__ == "__main__":
    while True:
        print("\n--- Welcome to ClinicAI ---")
        print("1. Patient Portal (Login/Sign-up)")
        print("2. Doctor Portal (Login)")
        print("3. Exit")
        
        portal_choice = input("Select Option: ")
        
        if portal_choice == "3":
            print("BOOM. Session closed. Keep building!")
            break

        username = input("Username: ")
        password = input("Password: ")
        
        active_user = None
        
        if username in users:
            if users[username].check_password(password):
                active_user = users[username]
            else:
                print("Invalid password.")
                continue
        else:
            if portal_choice == "1":
                print("No account found. Creating new patient profile...")
                full_name = input("Enter your full name: ")
                active_user = User(username, password, "patient", full_name)
                users[username] = active_user
            elif portal_choice == "2":
                print("No account found. Creating new doctor profile...")
                full_name = input("Enter your full name: ")
                active_user = User(username, password, "doctor", full_name)
                users[username] = active_user
            else:
                print("Invalid portal choice.")
                continue

        if active_user:
            if active_user.role == "doctor":
                doctor_dashboard(active_user)
            else:
                patient_workflow(active_user)
            log_feedback()

        if input("\nStart another session? (y/n): ").lower() != 'y':
            print("BOOM. Session closed. Keep building!")
            break
