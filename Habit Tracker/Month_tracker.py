# pip install customtkinter
# pip install Pillow
import pickle

from datetimes import month_days, day_names_list, date_passed
from constants import month_names
import datetime as dt
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
import tkinter as tk
import math

IMAGE_PATH = 'images'  # to be used to find path
BUTTON_PADX, BUTTON_PADY = 0, 0
TITLE_PADX, TITLE_PADY = 30, 35


class MonthTracker:
    def __init__(self, activity, window, frame, month=dt.datetime.now().month, year=dt.datetime.now().year):
        self.activity = activity
        self.color = '#ffe57d'
        window.configure(bg=self.color)
        self.month_name, self.days_cnt, self.month_idx, self.year, self.day = month_days(month + 1, year)
        self.tracker = frame
        self.tracker.config(bg=self.color, padx=30, pady=35, width=600, height=400)

        self.dict_images = {}  # Dictionary of images of each button
        self.dict_buttons = {}  # Dictionary containing buttons based on coordinates
        self.image_ref = {0: IMAGE_PATH + '/inactive_button.png', 1: IMAGE_PATH + '/complete_button.png',
                          2: IMAGE_PATH + '/incomplete_button.png',
                          3: IMAGE_PATH + '/covered_button.png',
                          4: IMAGE_PATH + '/old_button.png'}
        self.days_labels = {}
        self.name_file = f'tracker.pkl'
        try:
            with open(self.name_file, 'rb') as f:
                print('Old dict_status setup')
                self.dict_ref = pickle.load(f)
                try:
                    self.dict_status = self.dict_ref[self.activity][
                        month_names[self.month_name - 1] + '_' + str(self.year)]
                except KeyError:
                    self.dict_status = {}
        except FileNotFoundError:
            print('New dict_status setup')
            self.dict_status = {}
        self.create_canvas()

    def change_color(self, date_id: int):
        status = (self.dict_status[date_id] + 1) % (len(self.image_ref) - 1)
        self.dict_status[date_id] = status
        img = Image.open(self.image_ref[status]).resize((45, 45))
        img_tk = ImageTk.PhotoImage(img)
        self.dict_buttons[date_id].config(image=img_tk)
        self.dict_buttons[date_id].image = img_tk

    def save(self):
        self.dict_user = {self.activity: {month_names[self.month_name - 1] + '_' + str(self.year): self.dict_status}}
        print('File struc', self.dict_user)
        answer = messagebox.askokcancel('Confirm save', 'Are you sure if you want to save your changes?')
        if answer:
            with open(self.name_file, 'wb') as f:
                pickle.dump(self.dict_user, f, pickle.HIGHEST_PROTOCOL)
            messagebox.showinfo('Progress saved',
                                f'Your tracker for {self.activity} for {month_names[self.month_name - 1]}, {self.year} '
                                f'has been saved')

    def create_canvas(self):
        # ------------------------------------------- CREATE TITLE LABEL ----------------------------------------------#
        title = Label(self.tracker,
                      text=f'Welcome to the {self.activity} tracker\n {month_names[self.month_name - 1]}, {self.year}',
                      fg='black', bg=self.color, bd=0, font=('Myriad Pro', 20, 'bold'), compound=tk.TOP)

        title.grid(row=0, column=0, columnspan=6, padx=TITLE_PADX, pady=TITLE_PADY, sticky='S')
        # ------------------------------------------- POPULATE FIRST COLUMN WITH NAME OF DAYS--------------------------#
        for i in range(1, 8):
            # idx = str(i) + '_' + str(0)
            # label_name = 'label' + idx
            self.days_labels[str(i)] = Label(self.tracker, text=day_names_list[i - 1], bg=self.color, bd=0,
                                             font=('Myriad Pro', 15, 'bold'))
            self.days_labels[str(i)].grid(row=i, column=0, sticky="W", padx=BUTTON_PADX, pady=BUTTON_PADY)
        # ------------------------------------------- POPULATE SECOND COLUMN BASED ON DAY WHEN MONTH STARTS------------#
        # -------- FOR IRRELEVANT DAYS (if month starts on Wednesday, Sun-Tues are irrelevant--------------------------#
        for i in range(1, self.day):
            img_idx = 4
            img_tk = ImageTk.PhotoImage(Image.open(self.image_ref[img_idx]).resize((45, 45)))
            self.dict_images[1000 + i] = img_tk
            button = Button(self.tracker, height=60, width=60, bg=self.color,
                            image=img_tk, bd=0,
                            compound=tk.CENTER, state='disabled')
            button.grid(row=i, column=1, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="E")
        # -------- FOR DAYS in FIRST WEEK (if month starts on Wednesday, Wed-Sat of first week-------------#
        date = 1
        for i in range(self.day, 8):
            if not date_passed(date, self.month_idx, self.year):
                disabled_status = True
                img_idx = 4
            else:
                disabled_status = False
                try:
                    img_idx = self.dict_status[date]
                except KeyError:
                    img_idx = 0
            image_tk = ImageTk.PhotoImage(Image.open(self.image_ref[img_idx]).resize((45, 45)))
            self.dict_images[date] = image_tk
            button = Button(self.tracker, height=60, width=60, bg=self.color,
                            text=str(date),
                            image=image_tk, bd=0,
                            font=('Myriad Pro', 15, 'bold'),
                            command=lambda button_id=date: self.change_color(button_id),
                            compound=tk.CENTER, state=DISABLED if disabled_status else NORMAL)
            self.dict_buttons[date], self.dict_status[date] = button, img_idx
            self.dict_buttons[date].grid(row=i, column=1, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="E")
            date += 1
        # ------------------------------------ FOR REST OF THE DAYS OF THE MONTH---------------------------------------#

        for j in range(2, math.ceil(self.days_cnt / 7) + 2):
            for i in range(1, 8):
                if date > self.days_cnt:
                    break
                if not date_passed(date, self.month_idx, self.year):
                    disabled_status = True
                    img_idx = 4
                else:
                    disabled_status = False
                    try:
                        img_idx = self.dict_status[date]
                    except KeyError:
                        img_idx = 0
                image_tk = ImageTk.PhotoImage(Image.open(self.image_ref[img_idx]).resize((45, 45)))
                self.dict_images[date] = image_tk
                button = Button(self.tracker, height=60, width=60, bg=self.color,
                                text=str(date),
                                image=image_tk, bd=0,
                                font=('Myriad Pro', 15, 'bold'),
                                command=lambda button_id=date: self.change_color(button_id),
                                compound=tk.CENTER, state=DISABLED if disabled_status else NORMAL)
                self.dict_buttons[date], self.dict_status[date] = button, img_idx
                self.dict_buttons[date].grid(row=i, column=j, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="E")
                date += 1

        save_button = Button(self.tracker, text='Save', command=self.save, width=15, font=('Myriad Pro', 15, 'bold'))
        save_button.grid(row=j + 2, column=0, columnspan=7, padx=15, pady=15, sticky="NS")

        self.tracker.mainloop()

# tkwin = Tk()
# tkwin.minsize(600, 600)
# tkwin.configure(bg='#ffe57d')
# Mt = MonthTracker(tkwin, 7, 2023)
#
#
# with open(Mt.name_file,'wb') as f:
#     pickle.dump(Mt.dict_status,f,pickle.HIGHEST_PROTOCOL)
