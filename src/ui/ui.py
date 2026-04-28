import db.storage as storage
from entities.coinflip import Coinflip


def print_menu():
    print("1 - Signup")
    print("2 - Login")
    print("3 - List users")
    print("4 - Flip a coin")
    print("0 - Quit")

def launch():
    print("Welcome to the probability visualizer!")
    print_menu()

    while (True):
        command = input("Command: ")

        if command == '1':
            while True:
                username = input("Username: ")
                password = input("Password: ")
                try:
                    storage.add_user(username, password)
                    break
                except Exception as e:
                    print(e)

        elif command == "2":
            print("Functionality not available")

        elif command == "3":
            for user in storage.userlist():
                print(user)

        elif command == "4":
            repeats= int(input("How many times? "))
            if repeats > 0:
                Coinflip.flipcoin(repeats)

        elif command == '0':
            print("Goodbye!")
            break
        else:
            print("Give a valid command")
