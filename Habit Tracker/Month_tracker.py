# pip install customtkinter
# pip install Pillow
import pickle

from datetimes import month_days, day_names_list
import datetime as dt
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
import tkinter as tk
import math

IMAGE_PATH = 'images'  # to be used to find path


class MonthTracker:
    def __init__(self, tk_window, month=dt.datetime.now().month, year=dt.datetime.now().year, orientation='vertical'):
        self.color = '#ffe57d'
        self.month_name, self.days_cnt, self.month_idx, self.year, self.day = month_days(month, year)
        self.tracker = Frame(tk_window)
        self.tracker.config(bg=self.color, padx=30, pady=35, width=400, height=400)
        self.tracker.pack()
        self.dict_images = {}  # Dictionary of images of each button
        self.dict_buttons = {}  # Dictionary containing buttons based on coordinates
        self.orientation = orientation
        self.image_ref = {0: IMAGE_PATH + 'inactive_button.png', 1: IMAGE_PATH + 'complete_button.png',
                          2: IMAGE_PATH + 'incomplete_button.png',
                          4: IMAGE_PATH + 'covered_button.png'}
        self.days_labels = {}
        self.create_canvas()

    def change_color(self, ref_id, image_tk):
        self.dict_buttons[ref_id].config(image=image_tk)
        self.dict_buttons[ref_id].image = image_tk

    def on_click(self, b_id: int):
        ref = 'button' + str(b_id)
        img = Image.open('images/complete_button.png').resize((45, 45))
        img_tk = ImageTk.PhotoImage(img)
        self.change_color(ref, img_tk)

    def create_canvas(self):
        # ------------------------------------------- CREATE TITLE LABEL ----------------------------------------------#
        title = Label(self.tracker,
                      text=f'Welcome to the Activity tracker\n {self.month_name}, {self.year}',
                      fg='black', bg=self.color, bd=0, font=('Myriad Pro', 20, 'bold'), compound=tk.TOP)

        title.grid(row=0, column=0, columnspan=5, padx=15, pady=35)
        # ------------------------------------------- POPULATE FIRST COLUMN WITH NAME OF DAYS--------------------------#
        for i in range(1, 8):
            print('Label i', i)
            idx = str(i) + '_' + str(0)
            label_name = 'label' + idx
            self.days_labels[label_name] = Label(self.tracker, text=day_names_list[i - 1], bg=self.color, bd=0,
                                                 font=('Myriad Pro', 15, 'bold'))
            self.days_labels[label_name].grid(row=i, column=0, sticky="W", padx=10, pady=15)
        print('No. of days', self.days_cnt)
        date = 1
        print(self.day)
        # ------------------------------------------- POPULATE SECOND COLUMN BASED ON DAY WHEN MONTH STARTS------------#
        # -------- FOR IRRELEVANT DAYS (if month starts on Wednesday, Sun-Tues are irrelevant--------------------------#
        for i in range(1, self.day):
            idx = str(i) + '_' + str(1)
            button_name = 'button' + idx
            img_name = 'image' + idx
            img = Image.open('images/old_button.png').resize((45, 45))
            image_tk = ImageTk.PhotoImage(img)
            self.dict_images[img_name] = image_tk
            # str_no = (i + j * 7)
            self.dict_buttons[button_name] = Button(self.tracker, height=60, width=60, bg=self.color,
                                                    image=self.dict_images[img_name], bd=0,
                                                    compound=tk.CENTER, state='disabled')
            self.dict_buttons[button_name].grid(row=i, column=1, padx=5, pady=15, sticky="E")
        # -------- FOR DAYS in FIRST WEEK (if month starts on Wednesday, Wed-Sat of first week--------------------------#
        for i in range(self.day, 8):
            idx = str(i) + '_' + str(1)
            button_name = 'button' + idx
            img_name = 'image' + idx
            img = Image.open('images/inactive_button.png').resize((45, 45))
            image_tk = ImageTk.PhotoImage(img)
            self.dict_images[img_name] = image_tk
            # str_no = (i + j * 7)
            self.dict_buttons[button_name] = Button(self.tracker, height=60, width=60, bg=self.color,
                                                    text=str(date),
                                                    image=self.dict_images[img_name], bd=0,
                                                    font=('Myriad Pro', 15, 'bold'),
                                                    command=lambda button_id=idx: self.on_click(button_id),
                                                    compound=tk.CENTER)
            self.dict_buttons[button_name].grid(row=i, column=1, padx=5, pady=15, sticky="E")
            print(i, 1)
            date += 1
        # ------------------------------------ FOR REST OF THE DAYS OF THE MONTH---------------------------------------#
        for j in range(2, math.ceil(self.days_cnt / 7)):
            for i in range(1, 8):
                if date > self.days_cnt:
                    break
                idx = str(i) + '_' + str(j)
                button_name = 'button' + idx
                img_name = 'image' + idx
                img = Image.open('images/inactive_button.png').resize((45, 45))
                image_tk = ImageTk.PhotoImage(img)
                self.dict_images[img_name] = image_tk
                # str_no = (i + j * 7)
                self.dict_buttons[button_name] = Button(self.tracker, height=60, width=60, bg=self.color,
                                                        text=str(date),
                                                        image=self.dict_images[img_name], bd=0,
                                                        font=('Myriad Pro', 15, 'bold'),
                                                        command=lambda button_id=idx: self.on_click(button_id),
                                                        compound=tk.CENTER)
                self.dict_buttons[button_name].grid(row=i, column=j, padx=5, pady=15, sticky="E")
                date += 1
        # self.dict_buttons[button_name].grid(row=j+1, column=i+1, padx=8, pady=8)
        date += 1
        print(self.dict_images.keys())

        self.tracker.mainloop()


tkwin = Tk()
# tkwin.minsize(600,600)
tkwin.configure(bg='#ffe57d')
Mt = MonthTracker(tkwin, 7, 2023)
name=f'activity+month+year.pkl'
with open(name,'wb') as f:
    pickle.dump(Mt,f,pickle.HIGHEST_PROTOCOL)
