# Nano Shopping List
# Useful sopping list creator with mail sender
#
# Krzysztof Jankowski
# (c)2016 P1X 

import os.path
from Tkinter import *
import cPickle as pickle
import smtplib
from email.mime.text import MIMEText
import time

def list_initialize():
	global log_data
	log_data = []
	if(os.path.isfile("save.p")):
		load_list_from_db()
	update_list()
	latest_status.set('Latest list opened from database.')

def save_list_to_db():
	global log_data
	pickle.dump( log_data, open( "save.p", "wb" ) )

def load_list_from_db():
	global log_data
	log_data = pickle.load( open( "save.p", "rb" ) )

def clear_list():
	global log_data
	log_data = []
	update_list()
	latest_status.set('List cleared')

def update_list():
	loglist.delete(0, END)
	for item, quantity, shop in log_data:
		loglist.insert(END, format_list_entry(quantity, item, shop))
	loglist.pack()

def format_list_entry(quantity, item, shop):
	list_entry = ''
	if quantity:
		list_entry += quantity + ' x  '
	list_entry += item
	if shop:
		list_entry += '  from ' + shop
	return list_entry.encode('ascii', 'ignore').decode('ascii')


def add_to_list():
	global log_data
	global equantity, eshop, eitem, latest_status

	item = new_item_name.get()
	quantity = new_item_quantity.get()
	shop = new_item_shop.get()
	if(item):
		log_data.append ([item, quantity, shop])
		update_list()
		save_list_to_db()
	eitem.delete(0, END)
	eshop.delete(0, END)
	equantity.delete(0, END)
	eitem.focus()
	latest_status.set('Item added to the list')

def save_plain_list():
	global log_data
	file_ = open('mail.txt', 'w')
	file_.write('Buy this:\n')
	for item, quantity, shop in log_data:
		file_.write('- ' + format_list_entry(quantity, item, shop) + '\n')
	file_.write('\n\n-- \nYour Nano Shopping List\n')
	file_.close()

def mail_shopping_list():
	mail_from = 'nanoshoppinglist@p1x.in'
	mail_to = 'w84death@gmail.com'
	save_plain_list()
	fp = open('mail.txt', 'rb')
	mail_msg = MIMEText(fp.read())
	fp.close()

	mail_msg['Subject'] = 'Nano Shopping List - ' + time.strftime("%d/%m/%Y")
	mail_msg['From'] = mail_from
	mail_msg['To'] = mail_to

	s = smtplib.SMTP('localhost')
	s.sendmail(mail_from, [mail_to], mail_msg.as_string())
	s.quit()
	latest_status.set('List mailed to ' + mail_to)

def dumb_callback():
	return

def make_window():
	global loglist, new_item_name, new_item_quantity, new_item_shop
	global equantity, eshop, eitem, latest_status

	win = Tk()
	win.wm_title("Nano Shopping List")
	fheader = Frame(win)
	fheader.pack()

	menu = Menu(win)
	win.config(menu=menu)

	mfile = Menu(menu)
	menu.add_cascade(label="List", menu=mfile)
	mfile.add_command(label="Send mail", command=mail_shopping_list)
	mfile.add_command(label="Save as txt file", command=save_plain_list)
	mfile.add_command(label="Clear list", command=clear_list)

	msettings = Menu(menu)
	menu.add_cascade(label="Settings", menu=msettings)
	msettings.add_command(label="Mail adresses", command=dumb_callback)
	msettings.add_command(label="Databases", command=dumb_callback)

	mabout = Menu(menu)
	menu.add_cascade(label="Info", menu=mabout)
	mabout.add_command(label="About", command=dumb_callback)
	mabout.add_command(label="Licence", command=dumb_callback)
	mabout.add_command(label="Contribute", command=dumb_callback)

	latest_status = StringVar()
	status = Label(win, textvariable=latest_status, bd=1, relief=SUNKEN, anchor=W)
	status.pack(side=BOTTOM, fill=X)

	ltitle = Label(fheader, text="Main shopping list:")
	ltitle.pack(side=LEFT, padx=10)

	flog = Frame(win)
	flog.pack()
	scroll = Scrollbar(flog, orient=VERTICAL)
	loglist = Listbox(flog, yscrollcommand=scroll.set, height=7, width=40)
	scroll.config(command=loglist.yview)
	scroll.pack(side=RIGHT, fill=Y)
	loglist.pack(side=LEFT, fill=BOTH, expand=1)

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
	btn_add = Button(fbuttons, text="Add", command=add_to_list)
	btn_edit = Button(fbuttons, text="Edit", command=dumb_callback)
	btn_remove = Button(fbuttons, text="Remove", command=dumb_callback)
	btn_edit.config(state='disabled')
	btn_remove.config(state='disabled')
	btn_add.pack(side=LEFT, padx=4)
	btn_edit.pack(side=LEFT, padx=4)
	btn_remove.pack(side=LEFT, padx=4)

	eitem.focus()
	return win

win = make_window()
list_initialize()
win.mainloop()