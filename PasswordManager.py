import os
import sys
import time
import json
import base64 as b64
import string
import random
import pyperclip

os.system("cls")

os.system("title Password Manager")


# 123
secretkey = input("What's the secret key\x1b[1;31m?\x1b[0m ")

def encrypt(message):
    lkey=len(secretkey)
    secret=[]
    num=0
    for each in message:
        if num>=lkey:
            num = num % lkey
        secret.append(chr(ord(each)^ord(secretkey[num])))
        num += 1
    return b64.b64encode("".join(secret).encode()).decode()

def decrypt(message):
    leter = b64.b64decode(message.encode()).decode()
    lkey = len(secretkey)
    string = []
    num = 0
    for each in leter:
        if num >= lkey:
            num = num%lkey
        string.append( chr( ord(each)^ord(secretkey[num]) ) )
        num+=1
    return "".join(string)

def genrandompassword(amount):
    characters = string.ascii_letters + string.punctuation + string.digits
    password = "".join(random.choice(characters) for x in range(amount))
    return password

banner = """\x1b[31m _____                             _    _____\n|  _  |___ ___ ___ _ _ _ ___ ___ _| |  |     |___ ___ ___ ___ ___ ___ \n|   __| .'|_ -|_ -| | | | . |  _| . |  | | | | .'|   | .'| . | -_|  _|\n|__|  |__,|___|___|_____|___|_| |___|  |_|_|_|__,|_|_|__,|_  |___|_|  \n                                                         |___|        \x1b[0m"""

while True:
    os.system("cls")
    print(banner)
    print("""\n\x1b[1;31m[\x1b[0m1\x1b[1;31m] \x1b[0mShow a password\n\x1b[1;31m[\x1b[0m2\x1b[1;31m]\x1b[0m Input a passowrd\n\x1b[1;31m[\x1b[0m3\x1b[1;31m]\x1b[0m Delete a password""")
    userChoice = input("\nChoice: ")
    if userChoice == "1":
        os.system("cls")
        i = 0
        print(banner)
        with open("PasswordData.json") as passwordDataRawFile:
            passwordDataFormatted = json.load(passwordDataRawFile)
        for entry in passwordDataFormatted:
            i += 1
            print(f"\x1b[1;31m[\x1b[0m{str(i)}\x1b[1;31m] \x1b[0m{entry}\x1b[0m")
        showingChoice = input("\nEntry: ")
        i = 0
        for entry in passwordDataFormatted:
            i += 1
            if i == int(showingChoice):
                print("\nSite Name\x1b[1;31m: \x1b[0m" + entry)
                print("Username\x1b[1;31m/\x1b[0mEmail\x1b[1;31m: \x1b[0m" + decrypt(passwordDataFormatted[entry]["Email"]))
                print("Password\x1b[1;31m: \x1b[0m" + decrypt(passwordDataFormatted[entry]["Password"]))
        input("\nHit Enter once you're finished...")
    elif userChoice == "2":
        os.system("cls")
        print(banner)
        nameOfSite = input("Name Of Site\x1b[1;31m:\x1b[0m ")
        temporaryEmail = input("Username\x1b[1;31m/\x1b[0mEmail\x1b[1;31m:\x1b[0m ")
        generatePassword = input("Would you like to generate a password\x1b[1;31m(\x1b[0mYes\x1b[1;31m/\x1b[0mNo\x1b[1;31m): \x1b[0m")
        if generatePassword.lower() == "yes":
            characterLimit = int(input("How many characters\x1b[1;31m?\x1b[0m "))
            temporaryPassword = genrandompassword(characterLimit)
            pyperclip.copy(temporaryPassword)
            print(f"Generated Password\x1b[1;31m:\x1b[0m {temporaryPassword}\nCopied to clipboard...")
            time.sleep(1.5)
        elif generatePassword.lower() != "yes":
            temporaryPassword = input("Password\x1b[1;31m:\x1b[0m ")
            temporaryPassword2 = input("Password\x1b[1;31m(\x1b[0mConfirm\x1b[1;31m)\x1b[1;31m:\x1b[0m ")
            while temporaryPassword != temporaryPassword2:
            	os.system("cls")
            	print("\x1b[0m[\x1b[1;31m!\x1b[0m] Passwords did not match. Please enter them again!")
            	temporaryPassword = input("Password\x1b[1;31m:\x1b[0m ")
            	temporaryPassword2 = input("Password\x1b[1;31m(\x1b[0mConfirm\x1b[1;31m)\x1b[1;31m:\x1b[0m ")
        encryptedEmail = encrypt(temporaryEmail)
        encryptedPassword = encrypt(temporaryPassword)
        try:
            with open("PasswordData.json", "r") as passwordDataRawFile:
                passwordDataFormattedJson = json.load(passwordDataRawFile)
                passwordDataFormattedJson[nameOfSite] = {}
                passwordDataFormattedJson[nameOfSite]["Email"] = encryptedEmail
                passwordDataFormattedJson[nameOfSite]["Password"] = encryptedPassword
                try:
                    passwordDataRawFile.close()
                except:
                    pass
            with open('PasswordData.json', 'w') as passwordDataRawFile:
                json.dump(passwordDataFormattedJson, passwordDataRawFile, indent=4)
                try:
                    passwordDataRawFile.close()
                except:
                    pass
        except Exception as e:
            print(e)
        print("\x1b[0m[\x1b[1;32m!\x1b[0m] Added your site data input successfully! Returning home...")
        time.sleep(1.5)
        os.system("cls")
    elif userChoice == "3":
        os.system("cls")
        i = 0
        print(banner)
        with open("PasswordData.json") as passwordDataRawFile:
            passwordDataFormatted = json.load(passwordDataRawFile)
        for entry in passwordDataFormatted:
            i += 1
            print(f"\x1b[1;31m[\x1b[0m{str(i)}\x1b[1;31m] \x1b[0m{entry}\x1b[0m")
        deletionChoice = input("\nEntry\x1b[1;31m:\x1b[0m ")
        i = 0
        deletionentry = ""
        for entry in passwordDataFormatted:
            i += 1
            try:
                if i == int(deletionChoice):
                    deletionentry = entry
            except:
                pass
        verification = input(f"Are you sure you want to delete your saved credentials for {entry}\x1b[1;31m(\x1b[0mYes\x1b[1;31m/\x1b[0mNo\x1b[1;31m):\x1b[0m ")
        if verification.lower() == "yes":
            del passwordDataFormatted[entry]
            with open('PasswordData.json', 'w') as passwordDataRawFile:
                json.dump(passwordDataFormatted, passwordDataRawFile, indent=4)
            print(f"\x1b[0m[\x1b[1;32m!\x1b[0m] Deleted {entry} successfully! Returning home...")
            time.sleep(2)
