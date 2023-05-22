from utils import plot_location, display_dist
from tkinter import *
from customtkinter import *
from PIL import Image, ImageTk
# !pip install Pillow, customtkinter, tkinter
# CustomTkInter by Tom Schimansky: https://github.com/TomSchimansky/CustomTkinter
app = CTk()
app.minsize(400, 400)

app.title('\tWelcome to the ISS Spotting App')
# ---------------------------------BACKGROUND IMAGE--------------------------------------------#
background_image = ImageTk.PhotoImage(Image.open('images/space4.png'))
background_label = Label(app, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)





RESIZE_WIDTH = 0.35
RESIZE_HEIGHT = 0.4
# ---------------------------------COVER IMAGE--------------------------------------------#
# welcome=Label(app,text='Welcome to the ISS Tracker !!! ', height=30, width=20)
# welcome.grid(row=0,column=0, columnspan=3)

# ----------------------------CREATE IMAGE FOR BUTTONS---------------------------------------#
find_iss_img = ImageTk.PhotoImage(Image.open('images/planet-earth_updated2.png').resize((40, 40), Image.LANCZOS))
find_dist_img = ImageTk.PhotoImage(Image.open('images/distance_updated.png').resize((40, 40), Image.LANCZOS))

show_location = CTkButton(master=app, image=find_iss_img, text='Show me the ISS location', width=190, height=40,
                          compound='left', command=plot_location, fg_color='#c600ff', hover_color='#79009c',
                          text_color='#ffffff', font=('Arial', 12, 'bold'))
show_location.grid(row=2, column=0, sticky='w', pady=205, padx=20)
how_far = CTkButton(master=app, image=find_dist_img, text='How far is the ISS from me', width=190, height=40,
                    compound='left', command=display_dist, fg_color='#e40000', hover_color='#940000',
                    text_color='#ffffff', font=('Arial', 12, 'bold'))
how_far.grid(row=2, column=2, sticky='e', pady=205, padx=20)

app.mainloop()
