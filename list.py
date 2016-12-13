class List:
    def __self__(self, database):
        self.list_array = database

    def add(self, quantity, item, shop):
        self.list_array.append([quantity, item, shop])

    def sort(self):
       self.list_array = sorted(self.list_array, key=lambda item: item[2])

    def reset(self):
        self.list_array = []

