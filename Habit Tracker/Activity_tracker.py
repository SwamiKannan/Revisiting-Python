import tkinter
from tkinter import *
import customtkinter
from customtkinter import *
from constants import months, month_names
from Month_tracker import MonthTracker
from tkinter import messagebox, simpledialog


class Activity():
    def __init__(self):
        self.window = Tk()
        self.window.title("Welcome to your activity tracker")
        self.window.config(padx=50, pady=50)
        self.acts = self.openfile()
        print(self.acts)
        self.option_frames = Frame(self.window)
        self.option_frames.grid(row=0, column=0)
        self.create_tracker()

    # ----------- Created list of activities-------------------------------#
    def openfile(self, file='activities.txt'):
        with open('activities.txt', 'r') as f:
            acts = f.read().split(',')
        return acts

    def month_callback(self, n):
        self.month = n

    def year_callback(self, n):
        self.year = n

    def act_callback(self, n):
        self.act = n

    def get_deets(self):
        schedule_frame = Frame(self.window,width=self.window.winfo_width()-50,borderwidth=0,highlightthickness=0)
        schedule_frame.grid(row=0, column=0)
        schedule_frame.tkraise()
        mt = MonthTracker(self.act, self.window, schedule_frame, month=int(month_names.index(self.month)), year=int(self.year))

    def delete_activity(self):
        status = 'The existing activities are:'
        status += '\n'.join(self.acts)
        status += '\n' + 'Which activity would you like to delete'
        name = simpledialog.askstring('Delete activity', ' Enter the name of your activity to be deleted')
        if name:
            if name.capitalize() in self.acts:
                self.acts.remove(name)
                with open('activities.txt', 'w') as f:
                    f.write(','.join(self.acts))
                    confirm = f'{name.capitalize()} has been removed'
                    messagebox.showinfo('Activity removed', confirm)
                self.acts = self.openfile()
                self.create_tracker()
            else:
                messagebox.showinfo('Incorrect activity', 'The activity chosen does not exist')

    def create_activity(self):
        name = simpledialog.askstring('New activity', ' Enter the name of your new activity')
        print('Acts inside create', self.acts)
        self.acts.append(name.capitalize())
        print(self.acts)
        with open('activities.txt', 'w') as f:
            f.write(','.join(self.acts))
        self.acts = self.openfile()
        self.create_tracker()

    def create_tracker(self):
        title = Label(self.option_frames, text='Welcome to your tracker',
                      font=('Myriad Pro', 20, 'bold'))
        title.grid(row=0, column=0, pady=30, columnspan=3)

        subtitle_existing = Label(self.option_frames, text='Choose an existing activity',
                                  font=('Myriad Pro', 15, 'bold'))
        subtitle_existing.grid(row=1, column=0, pady=30)

        subtitle_new = Label(self.option_frames, text='Create a new activity', font=('Myriad Pro', 15, 'bold'))
        subtitle_new.grid(row=1, column=2, pady=30)

        a = StringVar()
        a.set('Choose your activity')
        self.drop_act = OptionMenu(self.option_frames, a, self.acts[0], *self.acts[1:], command=self.act_callback)
        self.drop_act.config(width=20)
        self.drop_act.grid(row=2, column=0, pady=20)

        m = StringVar()
        m.set('Choose your month')
        self.months = month_names
        self.drop_month = OptionMenu(self.option_frames, m, self.months[0], *self.months[1:],
                                     command=self.month_callback)
        self.drop_month.config(width=20)
        self.drop_month.grid(row=3, column=0, pady=20)

        y = StringVar()
        y.set('Choose your year')
        self.years = [str(2020 + i) for i in range(20)]
        self.drop_year = OptionMenu(self.option_frames, y, self.years[0], *self.years[1:], command=self.year_callback)
        self.drop_year.config(width=20)
        self.drop_year.grid(row=4, column=0, pady=20)

        self.select = Button(master=self.option_frames, text='Select', command=self.get_deets)
        self.select.grid(row=5, column=0, pady=20)

        self.create = Button(master=self.option_frames, text='Create New activity', command=self.create_activity)
        self.create.grid(row=2, column=2, padx=20, pady=20)

        self.delete = Button(master=self.option_frames, text='Delete existing activity', command=self.delete_activity)
        self.delete.grid(row=4, column=2, padx=20, pady=20)

        self.select1 = Label(master=self.option_frames, width=20, text='             ')
        self.select1.grid(row=3, column=1)

        self.window.mainloop()


activity = Activity()
