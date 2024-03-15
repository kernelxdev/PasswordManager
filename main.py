import json
import os
import uuid

# Check if passwords.json exists and is not empty
if os.path.exists("passwords.json") and os.stat("passwords.json").st_size != 0:
    with open("passwords.json", "r") as file:
        database = json.load(file)
else:
    database = {}

def clear_screen():
    # Clear screen by printing enough newline characters
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("1. Add new Password")
    print("2. Check password")
    print("3. Exit")
    choice = int(input("What do you want to do?: "))
    
    if choice == 1:
        clear_screen()
        newpass = input("Enter password: ")
        random_id = str(uuid.uuid4())
        database[random_id] = newpass
        with open("passwords.json", "w") as file:
            json.dump(database, file)
        print("Successfully wrote password")
    elif choice == 2:
        clear_screen()
        print("Stored Passwords:")
        for key, value in database.items():
            print(f"ID: {key}, Password: {value}")
    elif choice == 3:
        break
    else:
        print("Invalid choice. Please choose again.")
