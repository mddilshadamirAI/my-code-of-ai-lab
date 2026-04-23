# Career Path Guide v2.0
name = input("Enter your name: ")
print(f"\nWelcome, {name}! Your startup journey starts here.")

print("Choose your goal:")
print("1. Engineer\n2. Doctor\n3. Scientist\n4. Teacher")

choice = input("Enter choice (1-4): ")

if choice == "1":
    print("Goal: Engineer. Focus on Math and Problem Solving.")
elif choice == "2":
    print("Goal: Doctor. Focus on Biology and Consistency.")
elif choice == "3":
    print("Goal: Scientist. Focus on Research and Curiosity.")
elif choice == "4":
    print("Goal: Teacher. Focus on Communication and Patience.")
else:
    print("Focus on finding your passion first!")

print("\n[Status: Saved to local workspace]")
print("wait for the next update")
