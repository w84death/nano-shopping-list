import filesystem
import config
import helpers
import mailing

fs = filesystem.Filesystem()
cfg = config.Config()
hlp = helpers.Helpers()
mail = mailing.Mailing()

def main():
    print_hello()

def print_hello():
    print('\n Nano Shopping List')
    print(' ------------------\n')

main()
