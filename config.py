class Config:
    def __init__(self):
        self.mail = {
                'from': 'NanoShoppingList@p1x.in',
                'to': 'w84death@gmail.com'}
        self.ui_size = {
                'small': [32, 12],
                'medium':[36, 18],
                'big': [48, 24]}
        self.file = {
                'data': 'shopping_list_data.p',
                'text': 'shopping_list.txt'}

    def get_mail(self, item):
        return self.mail[item]

    def get_ui_size(self, item):
        return self.ui_size[item]

    def get_file(self, item):
        return self.file[item]
