import storage


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
            print("Toiminnallisuus ei vielä voimassa")
        elif command == '2':
            username = input("Anna käyttäjänimi: ")
            if username != "":
                store1.add_user(username)
            else:
                print("Ei käypä nimi")
        elif command == "3":
            store1.list_users()
        elif command == '0':
            print("Hei hei!")
            break
        else:
            print("Anna hyväksyttävä komento listalta")
