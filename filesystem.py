import os.path
import cPickle as pickle
import helpers
import config

hlp = helpers.Helpers()
cfg = config.Config()

class Filesystem:
    def __init__(self):
        if(not os.path.isfile(cfg.get_file('data'))):
            self.save([])

    def save(self, list):
        pickle.dump( list, open(cfg.get_file('data'), 'wb'))

    def load(self):
        return pickle.load( open(cfg.get_file('data'), 'rb'))

    def save_plain_text(self, list_array):
        file_ = open(cfg.get_file('text'), 'w')
        file_.write('Buy this:\n')
        for item, quantity, shop in list_array:
            file_.write('- ' + hlp.format_list_entry(quantity, item, shop) + '\n')
            file_.write('\n\n-- \nYour Nano Shopping List\n')
        file_.close()


