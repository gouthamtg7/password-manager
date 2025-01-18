from tkinter import *
import random
from tkinter import messagebox
import json
import os

#create window
window = Tk()
window.title("Password Manager")
window.minsize(800,600)

#create generate password function
uppercase_alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
def generating_password():
    password = "".join(random.sample(uppercase_alphabets,12))
    password_box.delete(0,END)
    password_box.insert(0,password)
show_password_state = IntVar()
def ShowPassword():
    if password_box.cget('show') == '*':
        password_box.config(show='')  # Show the password
        show_password.config(text='Hide Password')  # Change button text
    else:
        password_box.config(show='*')  # Hide the password
        show_password.config(text='Show Password')




#create canvas
canvas = Canvas(width=800,height=600)
img = PhotoImage(file="logo.png")

canvas.create_image(300,150,image = img)

website_label = canvas.create_text(50,275,text="Website :",font=("Arial",15,"normal"))


email_username_label = canvas.create_text(80,315,text="Email/Username:",font=("Arial",15,"normal"))

password_label = canvas.create_text(55,350,text="Password:",font=("Arial",15,"normal"))

website_entry_box = Entry(width=40)
canvas.create_window(295,275,window=website_entry_box)

email_username_box = Entry(width=60)
canvas.create_window(355,315,window=email_username_box)

password_box = Entry(width = 40,show="*")
canvas.create_window(295,350,window=password_box)

generate_password = Button(text="Generate Password",highlightthickness=0,command=generating_password)
canvas.create_window(480,350,window=generate_password)

show_password = Checkbutton(text="Show password",command=ShowPassword,variable=show_password_state)
canvas.create_window(220,380,window=show_password)


#Check if any field is empty
def is_everything_correctly_filled():
    k=0
    if len(password_box.get())<8:
         messagebox.showerror(title="OOPS!",message="Password should be atleast 8 characters.")
    else :
        k+=1
    if len(website_entry_box.get())<1:
        messagebox.showerror(title="OOPS!", message="Website Field is Empty!")
    else:
        k += 1
    if len(email_username_box.get()) < 1:
        messagebox.showerror(title="OOPS!", message="Email/Username Field is Empty!")
    else :
        k+=1
    if k==3:
        return True
    else :
        return False

def save_info():
    website = (website_entry_box.get())
    email_or_username = (email_username_box.get())
    password = (password_box.get())
    data = {website:
                {"email_username":email_or_username,
                 "password":password}
            }
    if(is_everything_correctly_filled()==True):
        confirmation = messagebox.askyesno(title=website,message=f"Email/Username: {email_or_username}\nPassword: {password}\nDo you confirm they are the correct information?")
        if confirmation==True:
            file_path = "data.json"
            if not os.path.exists(file_path):
                data_file = open("data.json", mode="w")
                json.dump(data, data_file, indent=4)
                data_file.close()
            else:
                with open("data.json","r") as data_file:
                    previous_data = json.load(data_file)
                    previous_data.update(data)
                    with open("data.json","w") as data_file:
                         json.dump(previous_data,data_file,indent=4)
            messagebox.showinfo("Success", "Information saved successfully!")

add_button = Button(text= "Add",highlightthickness=0,width=60,bg="black",fg="white",command=save_info)
canvas.create_window(355,410,window=add_button)

pin ="6969"


def show_data():
    website = website_entry_box.get()
    with open("data.json","r") as data_file:
        data = json.load(data_file)
        with open("data.json", "r") as data_file:
            previous_data = json.load(data_file)
        if website in previous_data:
            email_username = previous_data[website]["email_username"]
            password = previous_data[website]["password"]
            messagebox.showinfo(title="PASSWORD MANAGER",message=f"Email/Username: {email_username}\nPassword: {password}")
        else :
            messagebox.showerror(title="OOPS!!", message="Data not found.")


def search_data():
    if len(website_entry_box.get())>0:
        pin_window = Toplevel(window)
        pin_window.title("Security Check")
        pin_window.minsize(width=200, height=100)

        enter_pin_label = Label(pin_window, text="ENTER PIN:", font=("Arial", 15, "bold"))
        enter_pin_label.grid(row=0, column=1, padx=(50, 0), columnspan=2)

        enter_pin_box = Entry(pin_window, width=20)
        enter_pin_box.grid(row=2, column=1, padx=(50, 0), columnspan=2)
        global pin

        def check_pin():
            if enter_pin_box.get() != pin:
                messagebox.showerror(title="OOPS!!", message="Incorrect Password")
            else:
                show_data()

        submit_button = Button(pin_window, text="Submit", command=check_pin)
        submit_button.grid(row=4, column=1, padx=(55, 0), pady=(10, 0))




search_button = Button(text="Find Password",highlightthickness=0,command=search_data)
canvas.create_window(480,275,window=search_button)

canvas.grid(row = 0,column = 1,padx = (225,0),pady=0)

window.mainloop()
