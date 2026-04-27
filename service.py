import hashlib

class User:
    def __init__(self, username, password, role, address=None, mobile_number=None):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role
        self.address = address
        self.mobile_number = mobile_number

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)

class Product:
    def __init__(self, name, price, seller):
        self.name = name
        self.price = price
        self.seller = seller

    def display_info(self):
        return f"📦 {self.name} | Seller: {self.seller} | Price: ₹{self.price}"

# In-memory databases
users = {
    # Sellers
    "seller1": User("seller1", "sellpass1", "seller"),
    "seller2": User("seller2", "sellpass2", "seller"),
    "seller3": User("seller3", "sellpass3", "seller"),
    "seller4": User("seller4", "sellpass4", "seller"),
    "seller5": User("seller5", "sellpass5", "seller"),
    # Buyers
    "buyer1": User("buyer1", "buypass1", "buyer"),
    "buyer2": User("buyer2", "buypass2", "buyer"),
    "buyer3": User("buyer3", "buypass3", "buyer"),
    "buyer4": User("buyer4", "buypass4", "buyer"),
    "buyer5": User("buyer5", "buypass5", "buyer"),
}

products_list = [
    Product("Laptop", 75000, "seller1"),
    Product("Smartphone", 25000, "seller1"),
    Product("Wireless Mouse", 1500, "seller2"),
    Product("Keyboard", 2500, "seller2"),
    Product("USB-C Hub", 3000, "seller3"),
    Product("Monitor", 15000, "seller3"),
    Product("Webcam", 5000, "seller4"),
    Product("Headphones", 4000, "seller4"),
    Product("T-Shirt", 500, "seller5"),
    Product("Coffee Mug", 300, "seller5"),
]

def add_product(seller_name):
    name = input("Enter product name: ")
    try:
        price = float(input("Enter product price: "))
        new_product = Product(name, price, seller_name)
        products_list.append(new_product)
        print(f"\'{name}\' has been added to the marketplace!")
    except ValueError:
        print("Invalid price. Please enter a number.")

def view_seller_products(seller_name):
    print(f"\n--- Your Products ({seller_name}) ---")
    if not any(p.seller == seller_name for p in products_list):
        print("You have not added any products yet.")
        return
    for p in products_list:
        if p.seller == seller_name:
            print(p.display_info())

def view_all_products():
    print("\n--- Available Products ---")
    for i, p in enumerate(products_list):
        print(f"{i}. {p.display_info()}")

def get_feedback():
    give_feedback = input("\nWould you like to provide feedback on your experience? (yes/no): ").lower()
    if give_feedback == 'yes':
        try:
            rating = int(input("Please rate your experience on a scale of 1 to 5: "))
            review = input("Please provide a short review: ")
            
            if rating == 5:
                message = "Thank you for the 5-star rating and your amazing feedback! We're thrilled you had an excellent experience."
            elif rating == 4:
                message = "Thank you for the 4-star rating and your feedback! We're glad you had a good experience."
            elif 1 <= rating <= 3:
                message = f"Thank you for your {rating}-star rating and feedback. We are sorry to hear that you had a poor experience and will use your feedback to improve our system."
            else:
                message = "Invalid rating. Rating must be between 1 and 5."
            
            print(message)
            # In a real application, you would save the rating and review to a database.
            if 1 <= rating <= 5:
                print("Your review has been recorded.")

        except ValueError:
            print("Invalid input for rating. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    print("--- 🚀 Welcome to the Super App Marketplace ---")
    uname = input("Username: ")
    pword = input("Password: ")

    active_user = None

    if uname in users:
        if users[uname].check_password(pword):
            active_user = users[uname]
        else:
            print("Invalid password.")
            active_user = None 
    else:
        print(f"User \'{uname}\' not found. Let\'s create an account for you.")
        role = ""
        while role not in ['buyer', 'seller']:
            role = input("Are you a 'buyer' or a 'seller'? ").lower()
            if role not in ['buyer', 'seller']:
                print("Invalid role. Please enter 'buyer' or 'seller'.")
        
        new_user = User(uname, pword, role)
        users[uname] = new_user
        active_user = new_user
        print(f"Account for \'{uname}\' created as a {role}.")

    if active_user:
        print(f"\nWelcome, {active_user.username}! You are logged in as a {active_user.role}.")

        if active_user.role == 'buyer':
            while True:
                view_all_products()
                buy_choice = input("\nWould you like to buy a product? (yes/no): ").lower()
                if buy_choice == 'yes':
                    try:
                        idx = int(input("Enter Product ID to buy: "))
                        if 0 <= idx < len(products_list):
                            product = products_list[idx]
                            print(f"You are buying a {product.name} for ₹{product.price}.")
                            address = input("Enter your delivery address: ")
                            mobile_number = input("Enter your mobile number: ")
                            active_user.address = address
                            active_user.mobile_number = mobile_number
                            print("\n--- Purchase Confirmation ---")
                            print(f"🎉 You just bought a {product.name} for ₹{product.price}!")
                            print(f"It will be delivered to: {active_user.address}")
                            print(f"We will contact you at: {active_user.mobile_number} if needed.")
                            print(f"Thanks for your purchase, {active_user.username}!")
                        else:
                            print("Invalid product ID.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                else:
                    break
                
                another_purchase = input("\nWould you like to buy another product? (yes/no): ").lower()
                if another_purchase != 'yes':
                    break
            
            get_feedback()
            print("\nGoodbye!")

        elif active_user.role == 'seller':
            while True:
                choice = input("\nWhat would you like to do?\n1. Add a Product\n2. View Your Products\n3. Exit\nEnter option: ")
                if choice == "1":
                    add_product(active_user.username)
                elif choice == "2":
                    view_seller_products(active_user.username)
                elif choice == "3":
                    break
                else:
                    print("Invalid option selected.")
            
            get_feedback()
            print("\nGoodbye!")
