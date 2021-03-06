# Nano Shopping List
# Useful sopping list with mail sender
#
# github: https://github.com/w84death/nano-shopping-list
# donate:
# - bitcoin wallet address: 18oHovhxpevALZFcjH3mgNKB1yLi3nNFRY
# - paypal adress: w84death@gmail.com
#
# Krzysztof Jankowski
# (c)2016 P1X

import os.path
import time
from Tkinter import *
import cPickle as pickle
import smtplib
from email.mime.text import MIMEText

last_selected_item = -1
config = [
        ['nanoshoppinglist@p1x.in', 'w84death@gmail.com'], # mail from, mail to
        ['main', 'second'] # default shopping lists
        ]

def initialize_db():
    global shopping_list_array
    shopping_list_array = []
    if(os.path.isfile("save.p")):
        load_list_from_db()
    else:
        save_list_to_db()
    if(os.path.isfile("config.p")):
        load_config_from_db()
    else:
        save_config_to_db()

def load_default_list():
    load_list_from_db()
    update_list()
    latest_status.set('Latest list opened from database.')

def save_list_to_db():
    global shopping_list_array
    pickle.dump( shopping_list_array, open( "save.p", "wb" ) )

def load_list_from_db():
    global shopping_list_array
    shopping_list_array = pickle.load( open( "save.p", "rb" ) )

def save_config_to_db():
    global config
    pickle.dump( config, open( "config.p", "wb" ) )

def load_config_from_db():
    global config
    config = pickle.load( open( "config.p", "rb" ) )

def clear_list():
    global shopping_list_array
    shopping_list_array = []
    update_list()
    latest_status.set('List cleared but not saved. Restart to recover.')

def sort_list_array():
    global shopping_list_array
    shopping_list_array = sorted(shopping_list_array, key=lambda item: item[2])

def update_list():
    lbshopping.delete(0, END)
    sort_list_array()
    for item, quantity, shop in shopping_list_array:
        lbshopping.insert(END, format_list_entry(quantity, item, shop))
    lbshopping.pack()
    lbshopping.yview(END)

def format_list_entry(quantity, item, shop):
    list_entry = ''
    if shop:
        list_entry += shop + ' > '
    else:
        list_entry += '* > '
    list_entry += item
    if quantity:
        list_entry += ' (' + quantity + ')'
    return list_entry.encode('ascii', 'ignore').decode('ascii')

def add_to_list():
    global shopping_list_array
    global new_item_name, new_item_quantity, new_item_shop

    item = new_item_name.get()
    quantity = new_item_quantity.get()
    shop = new_item_shop.get()
    if(item):
        shopping_list_array.append ([item, quantity, shop])
        update_list()
        save_list_to_db()
        clear_inputs_and_focus()
        latest_status.set('Item added to the list')
    else:
        latest_status.set('Item name is requited!')

def clear_inputs_and_focus():
    global equantity, eshop, eitem, last_selected_item
    eitem.delete(0, END)
    eshop.delete(0, END)
    equantity.delete(0, END)
    eitem.focus()
    last_selected_item = -1

def selected_item():
    global lbshopping
    if lbshopping.curselection():
        return int(lbshopping.curselection()[0])
    else:
        return False

def is_item_selected():
    global lbshopping
    return lbshopping.curselection()


def load_selected_item():
    global shopping_list_array, last_selected_item
    global new_item_name, new_item_quantity, new_item_shop, eitem
    if is_item_selected():
        last_selected_item = selected_item()
        item, quantity, shop = shopping_list_array[last_selected_item]
        new_item_quantity.set(quantity)
        new_item_name.set(item)
        new_item_shop.set(shop)
        update_input_buttons()
        eitem.focus()
    latest_status.set('Item ready to edit. Update without edits to cancel.')

def update_item_in_list():
    global shopping_list_array, edit_mode, last_selected_item
    global new_item_name, new_item_quantity, new_item_shop
    if last_selected_item > -1:
        shopping_list_array[last_selected_item] = [new_item_name.get(), new_item_quantity.get(), new_item_shop.get()]
        update_list()
        save_list_to_db()
        clear_inputs_and_focus()
        update_input_buttons()
        latest_status.set('Item updated. List saved.')

def remove_item_in_list():
    global shopping_list_array
    if is_item_selected():
        del shopping_list_array[selected_item()]
        update_list()
        save_list_to_db()
        clear_inputs_and_focus()
        latest_status.set('Item removed. List saved.')


def save_plain_list():
    global shopping_list_array
    file_ = open('plain-list.txt', 'w')
    file_.write('Buy this:\n')
    for item, quantity, shop in shopping_list_array:
        file_.write('- ' + format_list_entry(quantity, item, shop) + '\n')
    file_.write('\n\n-- \nYour Nano Shopping List\n')
    file_.close()
    latest_status.set('Shopping list saved to plain-list.txt.')

def mail_shopping_list():
    global config
    mail_from = config[0][0]
    mail_to = config[0][1]
    save_plain_list()
    fp = open('plain-list.txt', 'rb')
    mail_msg = MIMEText(fp.read())
    fp.close()

    mail_msg['Subject'] = 'Nano Shopping List - ' + time.strftime("%d/%m/%Y")
    mail_msg['From'] = mail_from
    mail_msg['To'] = mail_to

    s = smtplib.SMTP('127.0.0.1', 25)
    s.sendmail(mail_from, [mail_to], mail_msg.as_string())
    s.quit()
    latest_status.set('List mailed to ' + mail_to)

def dumb_callback():
    return

def update_input_buttons():
    global bupdate, badd, last_selected_item
    if last_selected_item > -1:
        badd.config(state='disabled')
        bupdate.config(state='normal')
    else:
        badd.config(state='normal')
        bupdate.config(state='disabled')

def list_resize(new_width, new_height):
    global lbshopping
    lbshopping.config(width=new_width, height=new_height)
    lbshopping.pack()


def view_small_list():
    list_resize(32, 12)

def view_medium_list():
    list_resize(36, 18)

def view_big_list():
    list_resize(40, 24)

def make_window():
    global lbshopping, scroll, new_item_name, new_item_quantity, new_item_shop
    global equantity, eshop, eitem, latest_status, bupdate, badd

    win = Tk()
    win.wm_title("Nano Shopping List")
    fheader = Frame(win)
    fheader.pack()

    menu = Menu(win)
    win.config(menu=menu)

    mfile = Menu(menu)
    menu.add_cascade(label="List", menu=mfile)
    mfile.add_command(label="Send to " + config[0][1], command=mail_shopping_list)
    mfile.add_command(label="Save as txt file", command=save_plain_list)
    mfile.add_command(label="Clear list", command=clear_list)

    mselected = Menu(menu)
    menu.add_cascade(label="Selected", menu=mselected)
    mselected.add_command(label="Edit item", command=load_selected_item)
    mselected.add_command(label="Remove item", command=remove_item_in_list)

    mview = Menu(menu)
    menu.add_cascade(label="View", menu=mview)
    mview.add_command(label="Small list", command=view_small_list)
    mview.add_command(label="Medium list", command=view_medium_list)
    mview.add_command(label="Big list", command=view_big_list)

    latest_status = StringVar()
    status = Label(win, textvariable=latest_status, bd=1, relief=SUNKEN, anchor=W)
    status.pack(side=BOTTOM, fill=X)

    ltitle = Label(fheader, text="Main shopping list:")
    ltitle.pack(side=LEFT, padx=10)

    flog = Frame(win)
    flog.pack()
    scroll = Scrollbar(flog, orient=VERTICAL)
    lbshopping = Listbox(flog, yscrollcommand=scroll.set, height=18, width=36)
    scroll.config(command=lbshopping.yview)
    scroll.pack(side=RIGHT, fill=Y)
    lbshopping.pack(side=LEFT, fill=BOTH, expand=1)

    gitem = LabelFrame(win, text="Shoping item", padx=4, pady=4)
    gitem.pack(padx=10, pady=10)

    finput = Frame(gitem)
    finput.pack()
    Label(finput, text="Name: ").grid(row=1, column=0, sticky=W)
    Label(finput, text="Quantity: ").grid(row=2, column=0, sticky=W)
    Label(finput, text="Shop: ").grid(row=3, column=0, sticky=W)
    new_item_name = StringVar()
    new_item_quantity = StringVar()
    new_item_shop = StringVar()
    eitem = Entry(finput, textvariable=new_item_name)
    equantity = Entry(finput, textvariable=new_item_quantity)
    eshop = Entry(finput, textvariable=new_item_shop)
    eitem.grid(row=1, column=1)
    equantity.grid(row=2, column=1)
    eshop.grid(row=3, column=1)

    fbuttons = Frame(gitem)
    fbuttons.pack(pady=4)
    badd = Button(fbuttons, text="Add", command=add_to_list)
    bupdate = Button(fbuttons, text="Update", command=update_item_in_list)
    bupdate.config(state='disabled')
    badd.pack(side=LEFT, padx=4)
    bupdate.pack(side=LEFT, padx=4)

    eitem.focus()
    return win

win = make_window()
initialize_db()
load_default_list()
win.mainloop()
