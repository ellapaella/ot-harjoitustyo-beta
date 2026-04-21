import storage
from user import User
from coinflip import Coinflip


def print_menu():
    print("1 - Signup")
    print("2 - Login")
    print("3 - List users")
    print("4 - Flip a coin")
    print("0 - Quit")

def launch():
    store1 = storage.Storage()
    print("Welcome to the probability visualizer!")
    print_menu()

    while (True):
        command = input("Command: ")

        if command == '1':
            username = input("Username: ")
            if username != "":
                password = input("Password: ")
                if len(password) >= 8:
                    store1.add_user(User(username, password))
                else:
                    print("Password has to be at least 8 characters")
            else:
                print("Invalid username")

        elif command == "2":
            print("Functionality not available")

        elif command == "3":
            store1.list_users()

        elif command == "4":
            repeats= int(input("How many times? "))
            if repeats > 0:
                Coinflip.flipcoin(repeats)

        elif command == '0':
            print("Goodbye!")
            break
        else:
            print("Give a valid command")
