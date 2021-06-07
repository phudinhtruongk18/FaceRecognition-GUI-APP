class ListUserDetector(list):
    def __init__(self, all_employee_data):
        super().__init__()
        for employee in all_employee_data:
            self.append(UserDetector(employee))

    def show_list_users(self):
        for tempUser in self:
            print(tempUser.name)

    def find_index_by_id(self,id_to_check):
        for index,temp_user in enumerate(self):
            if temp_user.name == id_to_check:
                print(temp_user,id_to_check,"found")
                return index
        return None

    def add_backup_user(self, employee):
        self.append((UserDetector(employee)))


class UserDetector:
    def __init__(self, *args):
        if args.__len__() < 5:
            print("Wrong Employee Data!")
        self.counter = 0
        self.ID = args[0]
        self.name = args[1]
        self.sex = args[2]
        self.age = args[3]
        self.unit = args[4]

    def detect_user(self):
        self.counter += 8
