class ListUserDetector(list):
    def __init__(self, names):
        super().__init__()
        for name in names:
            self.append(UserDetector(name))

    def show_list_users(self):
        for tempUser in self:
            print(tempUser.name)

    def find_index_by_id(self,id_to_check):
        for index,temp_user in enumerate(self):
            if temp_user.name == id_to_check:
                return index
        return None

    def add_backup_user(self, id_to_add):
        self.append((UserDetector(id_to_add)))


class UserDetector:
    def __init__(self, name):
        self.counter = 0
        self.name = name

    def detect_user(self):
        self.counter += 8
