from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import random
import re

'''
CREDIT:
Show password icons created by Amazona Adorada at Flaticon (https://www.flaticon.com/free-icons/show-password)
'''

RESIZE_ICON = 0.7
SEGREGATION_SYNTAX = '???????'

app = Tk()
app.title('Welcome to your Offline Password Manager')
app.config(padx=50, pady=30)


def check_url(link):
    # Code referred from https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
    regex = re.compile(
        r'^(?:http|ftp|)s?://|www.'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, link) is not None


# ---------------------------- DATA ENCRYPTOR ------------------------------- #

def create_random_key():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    return key


# Check if private key has been generated else create private key
try:
    with open('filekey.key', 'r') as f:
        keys = f.read()
    print('Key available and read')
except FileNotFoundError:
    keys = create_random_key()
    messagebox.showinfo('No key found', 'New key generated. Old password files cannot be read')
fernet = Fernet(keys)


def open_decoded_file():
    # # Decode / encode logic was gleaned from https://stackoverflow.com/a/73350158
    data = []
    with open('pw_mgr.csv', 'r') as encrypted_file:
        # Decode / encode logic was gleaned from https://stackoverflow.com/a/73350158
        for line in encrypted_file:
            line_stripped = line.rstrip('\n')
            token_bytes = line_stripped.encode('utf-8')
            datastring = fernet.decrypt(token_bytes).decode('utf-8')
            sample = decrypt_text(datastring)[0]
            data.append(sample)
    return data


def encrypt_text(entries):
    with open('pw_mgr.csv', 'w', newline='\n') as encrypted:
        for entry in entries:
            data = SEGREGATION_SYNTAX.join(entry)
            data_bytes = data.encode('utf-8')
            token_bytes = fernet.encrypt(data_bytes)
            encrypted.write(token_bytes.decode('utf-8') + '\n')


def decrypt_text(text):
    decrypt_array = []
    decrypt_txt = text.split(SEGREGATION_SYNTAX)
    for i in range(0, len(decrypt_txt), 3):
        url = decrypt_txt[i]
        un = decrypt_txt[i + 1]
        pw = decrypt_txt[i + 2]
        decrypt_array.append([url, un, pw])
    return decrypt_array


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
specialchars = '!@#$%^&*()-=[]\\;\'/.,_+{}|":?><'
alphabet = letters + numbers + specialchars


def generate_pw():
    pw_length = random.randint(8, 15)
    pw = ''.join([random.choice(alphabet) for _ in range(pw_length)])
    print(pw)
    pw_field.insert(0, pw)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def validate_data(link, userid, password):
    # Requisite checks to ensure valid data has been passed to the appropriate fields
    if link or link.strip() != '':
        stat = check_url(link)
        if not stat:
            messagebox.showerror('Error in URL', 'You have entered an incorrect URL. Please re-enter the address')
            website_url.delete(0, END)
            return False
    else:
        messagebox.showerror('Error in URL', 'You have not entered a website. Please re-enter the address')
        return 0

    if not userid or userid.strip() is None:
        messagebox.showerror('Error in Username', 'You have not entered a username')
        un_field.delete(0, END)
        return False

    if not password or password.strip() is None:
        messagebox.showerror('Error in Password', 'You have not entered a password')
        pw_field.delete(0, END)
        return False

    isok = messagebox.askokcancel('Confirm details',
                                  f'Details entered are:\n\nWebsite:\t{link}\nUsername:\t{userid}\n\n Shall we proceed?')
    if not isok:
        website_url.delete(0, END)
        un_field.delete(0, END)
        pw_field.delete(0, END)
        return False

    return True


def save_pw():
    # get data from website_url, un_field and pw_field and check their validity
    url = website_url.get()
    un = un_field.get()
    pw = pw_field.get()
    if not validate_data(url, un, pw):
        return False
    entry = [url, un, pw]

    # Open the existing password manager file (pw_mgr.csv)and decrypt the data into decrypted array
    try:
        data = open_decoded_file()
        sample_exists = False  # Flag to check if an entry with the same url and username exists
        for sample_no in range(len(data)):
            sample = data[sample_no]
            # Update password if the same username already exists for the same url
            if sample[0] == url and sample[1] == un:
                data[sample_no][2] = pw  # Replace the passwird
                sample_exists = True
                break
            data.append(sample)
        if not sample_exists:
            data.append(entry)

    except FileNotFoundError:  # No password manager file exists (pw_mgr.csv) file exists to update the details to.
        print('New details file created')
        data = [entry]

    # Re-encrypt and close file
    encrypt_text(data)
    messagebox.showinfo("Success!", "Your password is saved")
    return 1


# ---------------------------- UI SETUP ------------------------------- #


logo_canvas = Canvas(app, width=200, height=200)
img = Image.open('eye.png')
image = img.resize((int(RESIZE_ICON * img.width), int(RESIZE_ICON * img.height)))
logo_img = ImageTk.PhotoImage(image)
logo_canvas.create_image(100, 100, image=logo_img)
logo_canvas.grid(row=0, column=1, sticky='', columnspan=2)

# Layout of text:"website"
website_text = Label(text='Website:')
website_text.grid(row=1, column=0, sticky='w', pady=5)

# Layout of website url
website_url = Entry(width=45)
website_url.grid(row=1, column=1, columnspan=2, sticky='w')  # Layout of website url
website_url.focus()

# Layout of text:"Email / username"
un_text = Label(text='Username / Email:', pady=5)
un_text.grid(row=2, column=0, sticky='w')

# Layout of field:"Email / username"
un_field = Entry(width=45)
un_field.grid(row=2, column=1, columnspan=2, sticky='w', pady=5)

# Layout of text:"Password"
pw_text = Label(text='Password:')
pw_text.grid(row=3, column=0, sticky='w')

# Layout of field:"Password"
pw_field = Entry(show='*', width=18)
pw_field.grid(row=3, column=1, sticky='w')

# Layout of button:"Generate Password"
pw_generate = Button(text='Generate Secure Password', padx=8, command=generate_pw)
pw_generate.grid(row=3, column=2, sticky=W)

# Layout of button:"Add Record"
add_button = Button(text='Add record', width=38, command=save_pw)
add_button.grid(row=4, column=1, columnspan=2, sticky=W, pady=5)

app.mainloop()
