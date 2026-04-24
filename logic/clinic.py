while True:
    print("Welcome to the patient support system")
    patient_name = input("What's your name? ")
    print(f"Welcome to our clinic, {patient_name.title()}")

    print("Please choose from the following symptoms:")
    print("1. Fever")
    print("2. Headache")
    print("3. Stomach pain")
    print("4. Other")

    try:
        symptom_choice = int(input("Enter the number of your symptom: "))
        if symptom_choice == 1:
            print("It sounds like you have a fever. We recommend you to drink plenty of fluids and rest. If the fever persists, please consult a doctor.")
        elif symptom_choice == 2:
            print("For a headache, you can try taking a pain reliever. If the headache is severe or persistent, please see a doctor.")
        elif symptom_choice == 3:
            print("For stomach pain, it's best to avoid solid foods for a few hours. If the pain is severe or you have other symptoms like nausea or vomiting, please seek medical attention.")
        elif symptom_choice == 4:
            other_symptom = input("Please describe your symptom: ")
            print(f"Thank you for sharing. For '{other_symptom}', we recommend you to schedule an appointment with one of our doctors for a proper diagnosis.")
        else:
            print("Invalid choice. Please enter a number from 1 to 4.")
    except ValueError:
        print("Invalid input. Please enter a number.")

    financial_help = input("Do you need financial help? (yes/no): ")
    if financial_help.lower() == 'yes':
        print("We have the following financial aid options available:")
        print("1. Government health programs")
        print("2. Care from other foundations")
        try:
            aid_choice = int(input("Please choose an option: "))
            if aid_choice == 1:
                print("You can find information about government health programs on the official government website.")
            elif aid_choice == 2:
                print("There are several foundations that offer financial assistance. You can search online for foundations that support patients with your condition.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("Thanks for giving your valuable time")
    print("If you have further more question feel free to ask ")

    another_patient = input("Do you want to add another patient? (yes/no): ")
    if another_patient.lower() != 'yes':
        break 

print("Thnks for using my tool!")
feed = int(input("If you want to give me feedback choose with a range of 1 to 5"))
if feed == 1:
   print("Thank you for your feedback, we will improve our system")
elif feed == 2:
     print("Thank you for your feedback, we will improve our system")
elif feed == 3:
     print("Thank you for your feedback, we will improve our system")
elif feed == 4:
     print("Thank you for your feedback, it's very good feeling to see you satisfied with our system ")
elif feed == 5:
     print("Thank you for your feedback, it's very good feeling to see you extremely satisfied with our system")

