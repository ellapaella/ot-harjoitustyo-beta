
class Storage():
    def __init__(self):
        self.storage = []

    def add_user(self, user):
        self.storage.append(user)

    def list_users(self):
        if len(self.storage) == 0:
            print("Ei käyttäjiä")
        else:
            for user in self.storage:
                print(user)

    def list_length(self):
        return len(self.storage)
