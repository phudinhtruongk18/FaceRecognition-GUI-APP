class ListEmployee(list):
    def __init__(self, all_employee_data):
        super().__init__()
        for employee in all_employee_data:
            self.append(Employee(*employee))

    def show_list_users(self):
        for tempUser in self:
            print(tempUser.name)

    def find_index_by_id(self,id_to_check):
        for index,temp_user in enumerate(self):
            if temp_user.ID == id_to_check:
                print(temp_user,id_to_check,"found")
                return index
        return None

    def add_backup_user(self, employee):
        self.append((Employee(employee)))


class Employee:

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


class Session:
    def __init__(self, *args):
        self.ID = args[0]
        self.name = args[1]
        self.duration = args[2]


class RecordDetail:
    def __init__(self, *args):
        self.ID = args[0]
        self.arrived_time = args[1]
        self.is_backup = args[2]
        self.id_employee = args[3]
        self.id_recorder = args[4]
