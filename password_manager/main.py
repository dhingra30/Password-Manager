from tkinter import *
from tkinter import messagebox
import random
import string
import json

LC_ALPHABETS = list(string.ascii_lowercase)
UC_ALPHABETS = list(string.ascii_uppercase)
SYMBOLS = list('~!@#$%^&*()_-+={[}]|;<,>.?/')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    screen.clipboard_clear()
    sym = [random.choice(SYMBOLS) for _ in range(2)]
    lc_alphabet = [random.choice(LC_ALPHABETS) for _ in range(9)]
    uc_alphabet = [random.choice(UC_ALPHABETS) for _ in range(1)]
    new_password = sym + lc_alphabet + uc_alphabet
    random.shuffle(new_password)
    password_string = ''
    for characters in new_password:
        password_string += characters
    enter_password.insert(0, password_string)
    screen.clipboard_append(password_string)


# ---------------------------- SEARCH DETAILS ------------------------------- #

def search_data():
    user_data = enter_website.get()
    with open("data.json", 'r') as data_file:
        new_data = json.load(data_file)
    try:
        enter_password.insert(0, new_data[user_data]['password'])
    except KeyError:
        messagebox.showerror(title="Does not exist", message=f"{user_data}, does not exist")
        answer = messagebox.askyesno(title="New Entry", message="Do you want to create one now? ")
        if answer:
            enter_password.delete(0, END)
            generate_password()
            save_to_file()
            messagebox.showinfo(title="Done", message="Save to file is completed")
        else:
            messagebox.showinfo(title="try again", message="try again")
    else:
        screen.clipboard_append(new_data[user_data]['password'])
        messagebox.showinfo(title="copied", message="Password has been copied to clipboard")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_to_file():
    web = enter_website.get()
    mail = enter_email.get()
    passwrd = enter_password.get()
    new_data = {web: {
        "email": mail,
        "password": passwrd
    }}
    if len(web) == 0 or len(mail) == 0:
        messagebox.showerror(title="Empty tabs", message="No Value entered for Website or Username/Email")
    else:
        try:
            with open("data.json", 'r') as data:
                # reading the old data from json file
                new_dat = json.load(data)
                # Updating the old data with new data
                new_dat.update(new_data)
        except FileNotFoundError:
            with open("data.json", 'w') as data:
                # Writing the updated data into json file
                json.dump(new_data, data, indent=4)
        else:
            with open("data.json", 'w') as data:
                # Writing the updated data into json file
                json.dump(new_dat, data, indent=4)
        finally:
            enter_website.delete(0, END)
            enter_password.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

screen = Tk()
screen.title('Password Manager')
screen.config(padx=20, pady=20)
canvas = Canvas(width=200, height=200)
photo_img = PhotoImage(file="logo.png")
canvas.create_image(150, 100, image=photo_img)
canvas.grid(row=0, column=1)
website = Label(text="Website:", font=('courier', 15))
website.grid(row=1, column=0)
enter_website = Entry(width=35, font=('courier', 15))
enter_website.grid(row=1, column=1, columnspan=2)
enter_website.focus()
email_username = Label(text="Email/Username:", font=('courier', 15))
email_username.grid(row=2, column=0)
enter_email = Entry(width=35, font=('courier', 15))
enter_email.insert(END, "rahuldhingraajd@gmail.com")
enter_email.grid(row=2, column=1, columnspan=2)
password = Label(text="Password:", font=('courier', 15))
password.grid(row=3, column=0)
enter_password = Entry(width=18, font=('courier', 15))
enter_password.grid(row=3, column=1)
password_generator = Button(text="Generate Password", width=13)
password_generator.grid(row=3, column=2)
password_generator.config(command=generate_password)
add = Button(text="Add", width=33)
add.grid(row=4, column=1, columnspan=2)
add.config(command=save_to_file)
search = Button(text="Search", width=13)
search.grid(row=1, column=3)
search.config(command=search_data)
screen.mainloop()
