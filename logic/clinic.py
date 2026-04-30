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
}

home_treatments = {
    "Fever": "Rest and drink plenty of fluids.",
    "Default": "Consult a doctor for an accurate diagnosis."
}

# --- Free API Engine (No Key Required) ---
def find_real_doctors(city, specialty):
    # Use a specific User-Agent so the free service doesn't block you
    headers = {
        'User-Agent': 'ClinicAI_Founder_App_Contact_mddilshad@gmail.com' 
    }
    
    # Try a different "Mirror" server if the first one is busy
    geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    
    try:
        # Step 1: Get City Coords
        geo_res = requests.get(geo_url, headers=headers).json()
        if not geo_res:
            print("Could not find city coordinates.")
            return []
        
        lat, lon = geo_res[0]['lat'], geo_res[0]['lon']

        # Step 2: Search for Doctors
        # We use a more stable mirror: 'https://overpass.kumi.systems/api/interpreter'
        overpass_url = "https://overpass.kumi.systems/api/interpreter"
        overpass_query = f"""
        [out:json][timeout:25];
        node["amenity"~"doctors|clinic"](around:10000,{lat},{lon});
        out body;
        """
        
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers)
        
        # Check if the response is actually JSON
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
        else:
            print(f"API Server returned error: {response.status_code}")
            return []

    except Exception as e:
        print(f"Connection Error: {e}")
        return []

# --- Workflows ---

def patient_workflow(user):
    print(f"\nWelcome, {user.full_name}!")
    
    symptoms_list = list(symptom_to_specialty.keys())
    for i, symptom in enumerate(symptoms_list, 1):
        print(f"{i}. {symptom}")
    
    try:
        choice = int(input("\nEnter the number for your symptom: "))
        if 1 <= choice <= len(symptoms_list):
            chosen_symptom = symptoms_list[choice - 1]
            specialty_needed = symptom_to_specialty[chosen_symptom]
            
            print(f"\nInitial Advice: {home_treatments.get(chosen_symptom, home_treatments['Default'])}")

            # --- FREE REAL WORLD SEARCH ---
            user.address = input("\nEnter your city (e.g., Patna, Bengaluru, Delhi): ")
            print(f"🚀 Searching OpenStreetMap for {specialty_needed} near {user.address}...")

            doctors = find_real_doctors(user.address, specialty_needed)

            if doctors:
                print(f"\n--- Real {specialty_needed}s Found Nearby ---")
                # Show top 5 results to keep terminal clean
                for doc in doctors[:5]:
                    print(f"👨‍⚕️ {doc['name']}")
                    print(f"⭐ {doc['rating']} | 📍 {doc['address']}\n")
            else:
                print(f"\nCould not find specific records for {specialty_needed} in {user.address} yet.")

        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")

def doctor_workflow(user):
    print(f"\nWelcome, Dr. {user.full_name}. You are logged into the ClinicAI Dashboard.")
    # In-memory feedback check
    print("1. View Patient Logs")
    if input("Choice: ") == "1":
        print("\n--- No recent logs found in this session ---")

# --- Main Application ---

if __name__ == "__main__":
    while True:
        print("\n--- Welcome to ClinicAI ---")
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        active_user = None
        if username in users:
            if users[username].check_password(password):
                active_user = users[username]
            else:
                print("Invalid password.")
        else:
            print("No account found. Creating new founder-patient profile...")
            full_name = input("Enter your full name: ")
            active_user = User(username, password, "patient", full_name)
            users[username] = active_user

        if active_user:
            if active_user.role == "patient":
                patient_workflow(active_user)
            else:
                doctor_workflow(active_user)
        
        if input("\nStart another session? (y/n): ").lower() != 'y':
            print("BOOM. Session closed. Keep building!")
            break
