class ListUserDetector(list):
    def __init__(self, names):
        super().__init__()
        for name in names:
            self.append(UserDetector(name))

    def show_list_users(self):
        for tempUser in self:
            print(tempUser.name)


class UserDetector:
    def __init__(self, name):
        self.counter = 0
        self.name = name

    def detect_user(self):
        self.counter += 8
