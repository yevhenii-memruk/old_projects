import threading
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sys

from data_base import DataServer
from check_price_player import PriceChecker

# create instance of Class
test = PriceChecker()
# initialize Tk() method
root = tk.Tk

# variables for working with PriceChecker
value_url = ""
value_delay = 0
value_percent = 0
football_players = []


class App(root):
    def __init__(self):
        super().__init__()

        self.title('Football Price Checker')
        self.geometry('500x400')
        self.resizable(0, 0)

        canvas1 = tk.Canvas(self, width=500, height=400, bg='#E8DCC4')
        canvas1.pack()

        # TITLE

        label_name = tk.Label(self, text='PRICE CHECKER', bg='#E8DCC4')
        label_name.config(font=('helvetica', 30))
        canvas1.create_window(250, 40, window=label_name)

        # URL ROW

        label_urls = tk.Label(self, text='Write full url: ', bg='#E8DCC4')
        label_urls.config(font=('Courier New', 14))
        canvas1.create_window(120, 90, window=label_urls)

        entry_urls = tk.Entry(self, bg="#F0F0F0")
        canvas1.create_window(300, 90, width=150, window=entry_urls)

        def add_url():
            global value_url
            try:
                value_url = str(entry_urls.get())
            except Exception as ex:
                print(ex)
            if value_url == "":
                pass
            else:
                football_players.append(value_url)

            entry_urls.delete(0, END)

            # DISPLAY ENTRY DATA
            data_entry = tk.Label(self, text=f'({len(football_players)})', fg="red", width=2, bg='#E8DCC4')
            data_entry.config(font=('helvetica', 10))
            canvas1.create_window(210, 90, window=data_entry)

        button_add_url = tk.Button(text='  ADD  ', command=add_url)
        button_add_url.config(font=('helvetica', 10))
        canvas1.create_window(440, 90, window=button_add_url)

        # DELAY ROW

        label_delay = tk.Label(self, text='Delay(sec): ', bg='#E8DCC4')
        label_delay.config(font=('Courier New', 14))
        canvas1.create_window(96, 125, window=label_delay)

        entry_delay = tk.Entry(self, bg="#F0F0F0")
        canvas1.create_window(300, 125, width=150, window=entry_delay)

        def input_delay():
            global value_delay
            try:
                value_delay = int(entry_delay.get())
            except Exception as ex:
                print(ex)
            entry_delay.delete(0, END)

            # DISPLAY DELAY DATA
            data_delay = tk.Label(self, text=f'({value_delay})', fg="red", width=2, bg='#E8DCC4')
            data_delay.config(font=('helvetica', 10))
            canvas1.create_window(210, 125, window=data_delay)

        button_delay = tk.Button(text='APPLY', command=input_delay)
        button_delay.config(font=('helvetica', 10))
        canvas1.create_window(440, 125, window=button_delay)

        # PERCENT ROW

        label_percent = tk.Label(self, text='Percent(%): ', bg='#E8DCC4')
        label_percent.config(font=('Courier New', 14))
        canvas1.create_window(96, 160, window=label_percent)

        entry_percent = tk.Entry(self, bg="#F0F0F0")
        canvas1.create_window(300, 160, width=150, window=entry_percent)

        def input_percent():
            global value_percent
            try:
                value_percent = int(entry_percent.get())
            except Exception as ex:
                print(ex)
            entry_percent.delete(0, END)

            # DISPLAY PERCENT DATA
            data_percent = tk.Label(self, text=f'({value_percent})', fg="red", width=2, bg='#E8DCC4')
            data_percent.config(font=('helvetica', 10))
            canvas1.create_window(210, 160, window=data_percent)

        button_percent = tk.Button(text='APPLY', command=input_percent)
        button_percent.config(font=('helvetica', 10))
        canvas1.create_window(440, 160, window=button_percent)

        # BUTTON "CLEAN"

        def clean_data():
            global value_percent
            global value_delay
            global football_players

            value_percent = 0
            value_delay = 0
            football_players.clear()

            input_percent()
            input_delay()
            add_url()

        button_clean = tk.Button(text="clean", command=clean_data, bg="#FFF982", height=2, width=6)
        button_clean.config(font=('helvetica', 15))
        canvas1.create_window(65, 340, window=button_clean)

        # BUTTON "START"

        def check_price_launcher(web_pages, delay, alert_percent):
            test.parse_info(web_pages, delay, alert_percent)

        def but_start():
            global thread
            print("Program starts executing...")

            # create thread for parallel execution check_price_player and interface
            thread = threading.Thread(target=check_price_launcher, args=[football_players, value_delay, value_percent])
            # create daemon to stop thread execution
            thread.daemon = True
            thread.start()

        def on_exit(self):
            """When you click to exit, this function is called"""
            if messagebox.askyesno("Exit", "Do you want to quit the application?"):
                self.quit()

        button_start = tk.Button(text='START', bg="#91FF80", width=10, height=1, command=but_start)
        button_start.config(font=('helvetica', 30))
        canvas1.create_window(250, 340, window=button_start)

        # TELEGRAM DATA

        # FRAME
        label_telegram = Label(self, text="TELEGRAM DATA", borderwidth=1, relief="solid", width=50, height=5, anchor=N)
        label_telegram.config(font=('helvetica', 12))
        canvas1.create_window(250, 238, window=label_telegram)

        label_token = tk.Label(self, text='TOKEN: ')
        label_token.config(font=('Courier New', 14))
        canvas1.create_window(70, 230, window=label_token)

        entry_token = tk.Entry(self)
        canvas1.create_window(260, 230, width=230, window=entry_token)

        label_chat_id = tk.Label(self, text='CHAT ID: ')
        label_chat_id.config(font=('Courier New', 14))
        canvas1.create_window(80, 260, window=label_chat_id)

        entry_chat_id = tk.Entry(self)
        canvas1.create_window(260, 260, width=230, window=entry_chat_id)

        def but_telegram():
            token = str(entry_token.get())
            chat_id = str(entry_chat_id.get())
            # make SQL query to update input data
            with DataServer() as db:
                query = f"UPDATE telegram_data SET token='{token}', chat_id='{chat_id}', num_id={1} WHERE num_id={1}"
                mycursor = db.cursor()
                mycursor.execute(query)
                db.commit()

        button_token = tk.Button(text='SAVE', bg="white", command=but_telegram, height=2)
        button_token.config(font=('helvetica', 10))
        canvas1.create_window(440, 245, window=button_token)

        # DISPLAY TELEGRAM DATA
        with DataServer() as db:
            query = f"SELECT * FROM telegram_data"
            mycursor = db.cursor()
            mycursor.execute(query)
            for i in mycursor:
                dis_token, dis_chat_id = i[0], i[1]

        entry_token.insert(0, dis_token)
        entry_chat_id.insert(0, dis_chat_id)

        # BUTTON "STOP"

        def but_stop():
            print("Stop program execution...")
            sys.exit()

        button_stop = tk.Button(text='stop', bg="#FF5F5F", width=6, height=2, command=but_stop)
        button_stop.config(font=('helvetica', 15))
        canvas1.create_window(434, 340, window=button_stop)


if __name__ == "__main__":
    app = App()
    app.mainloop()
