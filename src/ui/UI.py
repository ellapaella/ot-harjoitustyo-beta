import storage
from user import User
import graph


def print_menu():
    print("1 - Lisää toistokoe")
    print("2 - Luo uusi käyttäjä")
    print("3 - Listaa käyttäjät")
    print("0 - Lopeta")


def launch():
    store1 = storage.Storage()
    print("Tervetuloa todennäköisyysohjelmaan!")
    print_menu()

    while (True):
        command = input("Komento: ")

        if command == '1':
            nominator = input("Anna nimittäjä: ")
            denominator = input("Anna osoittaja: ")
            repeats = input("Anna toistojen määrä: ")
            coin_test = graph.Graph(nominator, denominator, repeats)

            to_whom = input("Kelle lisätään? ")

            for user in store1.storage:
                if user.name == to_whom:
                    user.add_graph(coin_test)

        elif command == '2':
            username = input("Anna käyttäjänimi: ")
            if username != "":
                password = input("Anna salasana: ")
                if len(password) > 8:
                    store1.add_user(User(username, password))
                else:
                    print("Salasanan oltava vähintään 8 merkkiä")
            else:
                print("Ei käypä nimi")
        elif command == "3":
            store1.list_users()
        elif command == '0':
            print("Hei hei!")
            break
        else:
            print("Anna hyväksyttävä komento listalta")
