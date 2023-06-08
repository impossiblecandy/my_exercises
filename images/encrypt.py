import pybase64
import pymysql
from tkinter import *
from tkinter import messagebox, ttk
import sys
from tkinter import Tk, Button, Toplevel
from tkinter.ttk import Treeview
from PIL import Image, ImageTk


# Establish MySQL connection
con = pymysql.connect(host="localhost", user="root", password="", database="login")
cur = con.cursor()

def clear():

    # Clear boxes
    my_text.delete(1.0, END)
    my_entry.delete(0, END)


def encrypt():
    # Get text from text box
    secret = my_text.get(1.0, END)
    # Clear the text box
    my_text.delete(1.0, END)

    # Logic for password
    if my_entry.get() == "turtle":
        # Convert to byte
        secret_byte = secret.encode("ascii")
        # Convert to base64
        encrypted_result = pybase64.b64encode(secret_byte)
        # Convert it back to ascii
        encrypted_result = encrypted_result.decode("ascii")
        # Print to text box
        my_text.insert(END, encrypted_result)

        # Save the input and the encrypted result to the MySQL database
        query = "INSERT INTO encryptions (result, pwd) VALUES (%s, %s)"
        values = (encrypted_result, secret)
        cur.execute(query, values)
        con.commit()

    else:
        # Flash a message if wrong password
        messagebox.showwarning("Incorrect!", "Incorrect Password, Try Again!")


def decrypt():
    # Get text from text box
    secret = my_text.get(1.0, END)
    # Clear the screen
    my_text.delete(1.0, END)

    # Logic for password
    if my_entry.get() == "turtle":
        # Convert to byte
        secret = secret.encode("ascii")
        # Convert to base64
        secret = pybase64.b64decode(secret)
        # Convert it back to ascii
        secret = secret.decode("ascii")
        # Print to text box
        my_text.insert(END, secret)

    else:
        # Flash a message if wrong password
        messagebox.showwarning("Incorrect!", "Incorrect Password, Try Again!")


def listEncryptions():
    try:
        # Retrieve encryptions from the database
        cur.execute("SELECT result FROM encryptions")
        results = cur.fetchall()

        my_text.delete(1.0, END)  # Clear the text box

        # Display the encryptions in the text box
        for result in results:
            my_text.insert(END, result[0] + '\n')

        # Open the update window
        openUpdateWindow()

    except Exception as e:
        print(str(e))
        sys.exit()


def openUpdateWindow():
    # Create a new window
    update_window = Toplevel(root)
    update_window.title("Update Encryptions")

    # Create a Treeview widget to display the data
    treeview = Treeview(update_window, style="Custom.Treeview")
    treeview.pack()

    # Define the custom style for Treeview
    treeview_style = ttk.Style()
    treeview_style.configure("Custom.Treeview", background="black", foreground="cyan")

    # Add columns to the Treeview
    treeview["columns"] = ("result", "pwd")
    treeview.heading("result", text="Result")
    treeview.heading("pwd", text="Password")

    # Populate the Treeview with data from the encryptions table
    cur.execute("SELECT * FROM encryptions")
    results = cur.fetchall()
    for result in results:
        treeview.insert("", "end", values=result)

    # Add buttons for delete and update operations
    delete_button = Button(update_window, text="Delete", command=lambda: deleteEntry(treeview), bg='#000000', fg="cyan")
    delete_button.pack(pady=10)

    # Update the Treeview after performing delete or update operations
    def refreshTreeview():
        treeview.delete(*treeview.get_children())
        cur.execute("SELECT * FROM encryptions")
        updated_results = cur.fetchall()
        for updated_result in updated_results:
            treeview.insert("", "end", values=updated_result)

    # Function to delete an entry from the encryptions table
    def deleteEntry(tree):
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item)
            result = item_values['values'][1]  # Get the value from the second column
            query = "DELETE FROM encryptions WHERE result=%s"
            cur.execute(query, (result,))
            con.commit()
            refreshTreeview()



root = Toplevel()
root.geometry("800x450")
root.title('Encryption')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (450 // 2)
root.geometry(f"800x450+{x}+{y}")

image = Image.open("background-5.png")
image = image.resize((800, 450))
photo = ImageTk.PhotoImage(image)
# Set Label with image as background
root_label = Label(root, image=photo)
root_label.place(x=0, y=0, relwidth=1, relheight=1)

enc_label = Label(root, text="Texto a encriptar/descriptar:", font=("courier", 18), bg="#000000", fg="cyan")
enc_label.pack(pady=25)

my_text = Text(root, width=57, height=10, bg='#000000', fg="white")
my_text.pack(pady=15)

password_label = Label(root, text="Contraseña...", font=("courier", 14), bg='#000000', fg="cyan")
password_label.pack()

my_entry = Entry(root, font=("courier", 18), width=35, show="*", bg='#000000', fg="cyan")
my_entry.pack(pady=10)

my_frame = Frame(root)
my_frame.pack(pady=20)

enc_button = Button(my_frame, text="Encrypt", font=("courier", 18), command=encrypt, bg='#000000', fg="cyan")
enc_button.grid(row=0, column=0)

dec_button = Button(my_frame, text="Decrypt", font=("courier", 18), command=decrypt, bg='#000000', fg="cyan")
dec_button.grid(row=0, column=1, padx=20)

clear_button = Button(my_frame, text="Clear", font=("courier", 18), command=clear, bg='#000000', fg="cyan")
clear_button.grid(row=0, column=2)

list_button = Button(my_frame, text="List", font=("courier", 18), command=listEncryptions, bg='#000000', fg="cyan")
list_button.grid(row=0, column=3, padx=20)


root.tk_setPalette(background='#000000', highlightBackground='#000000')


root.mainloop()

# Close MySQL connection
con.close()

