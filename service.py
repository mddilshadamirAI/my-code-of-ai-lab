print("---Welcome to our service---")
print("Here we connect the service provider to service seeker")
import hashlib
class User:
    def __init__(self, username, password):
        self.username = username
        # We store the HASH, never the plain password
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)
# Database of users (In 6 months, this will be a real SQL database!)
user_db = {
    "dilshad": User("dilshad", "founder2026")
}
class Service:
    def __init__(self, name, price_per_hour, provider_name):
        self.name = name
        self.price = price_per_hour
        self.provider = provider_name
        self.is_available = True

    def display_info(self):
        status = "Available" if self.is_available else "Busy"
        return f"🛠️ {self.name} | Provider: {self.provider} | Rate: ₹{self.price}/hr | Status: {status}"

class Booking:
    def __init__(self, username, service):
        self.username = username
        self.service = service
        self.service.is_available = False # When a service is booked, it becomes unavailable

    def get_receipt(self):
        return f"✅ Booking Confirmed for {self.username}! You hired {self.service.provider} for {self.service.name} at ₹{self.service.price}/hr."

class Product:
    def __init__(self, name, price, seller):
        self.name = name
        self.price = price
        self.seller = seller

    def display_info(self):
        return f"📦 {self.name} | Seller: {self.seller} | Price: ₹{self.price}"

# --- Initializing the App Data ---
# This is how you "add" services to your platform
services_list = [
    Service("Mobile Repair", 500, "mobile Tech"),
    Service("Home Cleaning", 300, "QuickClean Co."),
    Service("P2P Consult", 1000, "Founder Insights")
]

products_list = [
    Product("SuperApp T-Shirt", 499, "SuperApp Merch"),
    Product("Founder's Mug", 249, "SuperApp Merch"),
]

print("--- 🚀 Welcome to the Super App Engine ---")
for s in services_list:
    print(s.display_info())
for p in products_list:
    print(p.display_info())


def main_menu():
    print("\n--- 📱 Dilshad's SuperApp Terminal ---")
    print("1. View Available Services")
    print("2. Book a Service")
    print("3. View Products")
    print("4. Buy a Product")
    print("5. Exit")
    return input("Choose an option: ")

if __name__ == "__main__":
    # Simulate Login
    uname = input("Username: ")
    pword = input("Password: ")

    if uname in user_db and user_db[uname].check_password(pword):
        active_user = user_db[uname]
        while True:
            choice = main_menu()
            
            if choice == "1":
                for i, s in enumerate(services_list):
                    print(f"{i}. {s.display_info()}")
            
            elif choice == "2":
                idx = int(input("Enter Service ID to book: "))
                if services_list[idx].is_available:
                    booking = Booking(active_user.username, services_list[idx])
                    print(booking.get_receipt())
                else:
                    print("❌ Sorry, that provider is busy!")

            elif choice == "3":
                for i, p in enumerate(products_list):
                    print(f"{i}. {p.display_info()}")

            elif choice == "4":
                idx = int(input("Enter Product ID to buy: "))
                product = products_list[idx]
                print(f"🎉 You just bought a {product.name} for ₹{product.price}! Thanks for your purchase, {active_user.username}!")
            
            elif choice == "5":
                print("Goodbye, Founder!")
                break
    else:
        print("Access Denied.")