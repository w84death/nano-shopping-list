class Helpers:
   def format_entry(self, quantity, item, shop):
        formated_entry = ''
        if shop:
            formated_entry += shop + ' > '
        else:
            formated_entry += '* > '
        formated_entry += item
        if quantity:
            formated_entry += ' (' + quantity + ')'
        return formated_entry.encode('ascii', 'ignore').decode('ascii') 
