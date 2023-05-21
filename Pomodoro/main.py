from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
WORK = '#202A44'
SHORT_BREAK = '#006A4E'
LONG_BREAK = '#f6602d'

window = Tk()
window.minsize(600,600)
img_layout = Canvas(height=240, width=224, bd=0, bg=YELLOW, highlightthickness=0)
ticks_txt = '00:00'
# series = []
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    global series
    series = []
    global ticks_txt
    ticks_txt = ''
    img_layout.itemconfig(clock, text=f'00:00')
    app_title['text'] = 'Pomodoro'


def start():
    global series
    series = []
    check_countdown()


def check_countdown():
    long_break_series = ['work', 'short_break', 'work', 'short_break', 'work', 'short_break', 'work']
    global ticks_txt
    print(series)
    tick_count = series.count('work')
    ticks_txt = '✔' * tick_count
    ticks['text'] = ticks_txt
    if series:
        if series[-1] == 'work':
            if len(series) >= 7 and series[-7:] == long_break_series:
                countdown_longbreak()
            else:
                countdown_shortbreak()
        else:
            countdown_work()
    else:
        countdown_work()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def countdown_work():
    app_title['text'] = 'Work'
    app_title['fg'] = WORK
    countdown(WORK_MIN * 60)
    series.append('work')


def countdown_shortbreak():
    app_title['text'] = 'Taking a short break ..... '
    app_title['fg'] = SHORT_BREAK
    countdown(SHORT_BREAK_MIN * 60)
    series.append('short_break')


def countdown_longbreak():
    # ticks['text'] = ''
    print('Doing longbreak')
    app_title['text'] = 'Taking a longer break ..... '
    app_title['fg'] = LONG_BREAK
    countdown(LONG_BREAK_MIN * 60)
    series.append('long_break')


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    item_min = count // 60
    item_sec = count % 60
    if item_sec < 10:
        item_sec = '0' + str(item_sec)
    img_layout.itemconfig(clock, text=f'{item_min}:{item_sec}')
    if count == 0:
        check_countdown()
    else:
        global timer
        timer = window.after(1000, countdown, count - 1)


# ---------------------------- UI SETUP ------------------------------- #


window.title('Pomodoro')
window['padx'] = 100
window['pady'] = 20
# window.minsize(600, 600)
window['bg'] = YELLOW
# SETUP TITLE
app_title = Label()
app_title['text'] = 'Pomodoro'
app_title['font'] = ('Arial', 24, 'bold')
app_title['bg'] = YELLOW
app_title['fg'] = GREEN
app_title.grid(column=1, row=0, sticky="S")
# SETUP MAIN IMAGE

img = PhotoImage(file='tomato.png')
img_layout.create_image(110, 120, image=img)
clock = img_layout.create_text(110, 140, text='00:00', font=(FONT_NAME, 24, 'bold'))
img_layout.grid(column=1, row=1, sticky="S")
# SETUP START
start = Button(text='Start', font=('Arial', 24, 'bold'), command=start)
start['bg'] = YELLOW
start.grid(column=0, row=2, pady=50, sticky="E")
reset = Button(text='Reset', font=('Arial', 24, 'bold'), command=reset_timer)
reset['bg'] = YELLOW
reset.grid(column=2, row=2, pady=50, sticky="W")
ticks = Label(text=ticks_txt, font=('Arial', 12, 'bold'))
ticks['bg'] = YELLOW
ticks.grid(column=1, row=3)

window.mainloop()
