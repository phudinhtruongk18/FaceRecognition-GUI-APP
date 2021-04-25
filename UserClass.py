
class ListUserDetector(list):
    def __init__(self, names):
        super().__init__()
        for name in names:
            self.append(UserDetector(name))

    def xemDanhSach(self):
        for tempUser in self:
            print(tempUser.name)


class UserDetector:
    def __init__(self, name):
        self.counter = 0
        self.name = name

    def xac_nhan_nguoi_dung(self):
        self.counter += 1
