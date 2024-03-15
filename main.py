import json
import os
import uuid

# Load existing passwords if any
try:
    with open("passwords.json", "r") as file:
        database = json.load(file)
except FileNotFoundError:
    database = {}

while True:
    print("1. Add new Password")
    print("2. Check password")
    print("3. Exit")
    choice = int(input("What do you want to do?: "))
    
    if choice == 1:
        os.system("cls")  # For Windows. For Linux, use "clear"
        newpass = input("Enter password: ")
        random_id = str(uuid.uuid4())
        database[random_id] = newpass
        with open("passwords.json", "w") as file:
            json.dump(database, file)
        print("Successfully wrote password")
    elif choice == 2:
        os.system("cls")  # For Windows. For Linux, use "clear"
        print("Stored Passwords:")
        for key, value in database.items():
            print(f"ID: {key}, Password: {value}")
    elif choice == 3:
        break
    else:
        print("Invalid choice. Please choose again.")
