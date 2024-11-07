import json
import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from getpass import getpass
import random
import string

def generate_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
    return kdf.derive(password.encode())

def encrypt_password(password: str,key: bytes):
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    encrypted_password = aesgcm.encrypt(nonce,password.encode(), None)
    return base64.b64encode(nonce + encrypted_password).decode()

def decrypt_password(encrypted_password: str, key: bytes):
    encrypted_password_bytes = base64.b64decode(encrypted_password)
    nonce = encrypted_password_bytes[:12]
    ciphertext = encrypted_password_bytes[12:]

    aesgcm = AESGCM(key)
    try:
        decrypted_password = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_password.decode()
    except InvalidTag:
        return None

def load_password_database(filename='passwords.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_password_database(database, filename='passwords.json'):
    with open(filename, 'w') as f:
        json.dump(database, f, indent=4)

def generate_password(length=32):
    # Add function to be able to choose the lenght of new password

    letters = string.ascii_letters
    digits = string.digits
    special_chars = "!@#$%&*" # Decided to use these so the password looks more natural

    password = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars)
    ]

    all_chars = letters + digits + special_chars
    password += random.choices(all_chars, k=length - 3)

    random.shuffle(password)
    return ''.join(password)

def password_manager():
    database = load_password_database()

    master_password = getpass("Enter your master password: ")

    salt = b'\x00' * 16
    key = generate_key(master_password, salt)

    while True:
        print("\n1. Store a new password\n2. Retrieve a password\n3. Generate a strong password and store it\n4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            service = input("Enter the name of the service: ")
            password = getpass("Enter the password to store: ")

            encrypted_password = encrypt_password(password, key)
            database[service] = encrypted_password
            save_password_database(database)
            print(f"Password for {service} stored successfully.")

        elif choice == '2':
            service = input("Enter the name of the service: ")
            if service in database:
                encrypted_password = database[service]
                decrypted_password = decrypt_password(encrypted_password, key)
                if decrypted_password:
                    print(f"The password for {service} is: {decrypted_password}")
                else:
                    print("Incorrect master password or corrupted data.")
            else:
                print("No password stored for that service.")

        elif choice == '3':
            service = input("Enter the name of the service: ")
            password = generate_password()

            encrypted_password = encrypt_password(password, key)
            database[service] = encrypted_password
            save_password_database(database)
            print(f"Password for {service} generated successfully.")

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    password_manager()
