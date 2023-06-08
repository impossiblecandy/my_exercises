from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import pymysql


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login y Sign in")
        self.root.geometry("1366x700+0+0")
        self.root.resizable(False, False)
        self.loginform()

    def loginform(self):
        Frame_login = Frame(self.root, bg="black")
        Frame_login.place(x=0, y=0, height=700, width=1366)
        self.img = ImageTk.PhotoImage(file="background-2.png")
        img = Label(Frame_login, image=self.img).place(x=0, y=0, width=1366, height=700)

        frame_input = Frame(self.root, bg='black')
        frame_input.place(x=320, y=130, height=450, width=400)

        label1 = Label(frame_input, text="Login", font=('courier', 32, 'bold'), fg="cyan", bg='black')
        label1.place(x=75, y=20)

        label2 = Label(frame_input, text="Usuario", font=("courier", 20, "bold"), fg='cyan', bg='black')
        label2.place(x=30, y=95)

        self.email_txt = Entry(frame_input, font=("courier", 15, "bold"), bg='white')
        self.email_txt.place(x=30, y=145, width=270, height=35)

        label3 = Label(frame_input, text="Contraseña", font=("courier", 20, "bold"), fg='cyan', bg='black')
        label3.place(x=30, y=195)

        self.password = Entry(frame_input, font=("courier", 15, "bold"), bg='white',show='*')
        self.password.place(x=30, y=245, width=270, height=35)


        btn2 = Button(frame_input, text="Login", command=self.login, cursor="hand2", font=("courier", 15), fg="black", bg="cyan", bd=0, width=10, height=3)
        btn2.place(x=0, y=350)

        btn3 = Button(frame_input, command=self.Register, text="Registro", cursor="hand2", font=("courier", 15), bg='cyan', fg="black", bd=0, width=10, height=3)
        btn3.place(x=200, y=350)

    def login(self):
        if self.email_txt.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='', database='login')
                cur = con.cursor()
                cur.execute('select * from logintbl where user=%s and pwd=%s', (self.email_txt.get(), self.password.get()))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror('Error', 'Invalid Username And Password', parent=self.root)
                    self.loginclear()
                    self.email_txt.focus()
                else:
                    self.appscreen()
                con.close()
            except Exception as es:
                messagebox.showerror('Error', f'Error Due to : {str(es)}', parent=self.root)

    def Register(self):
        Frame_login1 = Frame(self.root, bg="black")
        Frame_login1.place(x=0, y=0, height=700, width=1366)
        self.img = ImageTk.PhotoImage(file="background-2.png")
        img = Label(Frame_login1, image=self.img).place(x=0, y=0, width=1366, height=700)

        frame_input2 = Frame(self.root, bg='black')
        frame_input2.place(x=280, y=130, height=450, width=630)

        label1 = Label(frame_input2, text="Registro", font=('courier', 32, 'bold'), fg="cyan", bg='black')
        label1.place(x=45, y=20)

        label2 = Label(frame_input2, text="Usuario", font=("courier", 20, "bold"), fg='cyan', bg='black')
        label2.place(x=30, y=95)

        self.entry = Entry(frame_input2, font=("courier", 15, "bold"), bg='lightgray')
        self.entry.place(x=30, y=145, width=270, height=35)

        label3 = Label(frame_input2, text="Contraseña", font=("courier", 20, "bold"), fg='cyan', bg='black')
        label3.place(x=30, y=195)

        self.entry2 = Entry(frame_input2, font=("courier", 15, "bold"), bg='lightgray')
        self.entry2.place(x=30, y=245, width=270, height=35)

        label4 = Label(frame_input2, text="Email-id", font=("courier", 20, "bold"), fg='cyan', bg='black')
        label4.place(x=330, y=95)

        self.entry3 = Entry(frame_input2, font=("courier", 15, "bold"), bg='lightgray')
        self.entry3.place(x=330, y=145, width=270, height=35)

        label5 = Label(frame_input2, text="Confirmar contraseña", font=("courier", 15, "bold"), fg='cyan', bg='black')
        label5.place(x=330, y=195)

        self.entry4 = Entry(frame_input2, font=("courier", 15, "bold"), bg='lightgray')
        self.entry4.place(x=330, y=245, width=270, height=35)

        btn2 = Button(frame_input2, command=self.register, text="Registrar", cursor="hand2", font=("courier", 15), fg="black", bg="cyan", bd=0, width=15, height=3)
        btn2.place(x=90, y=340)

        btn3 = Button(frame_input2, command=self.loginform, text="Login", cursor="hand2", font=("courier", 15), bg='cyan', fg="black", bd=0, width =15, height=3)
        btn3 = Button(frame_input2, command=self.loginform, text="Login", cursor="hand2", font=("courier", 15), bg='cyan', fg="black", bd=0, width =15, height=3)
        btn3.place(x=400, y=340)

    def register(self):
        if self.entry.get() == "" or self.entry2.get() == "" or self.entry3.get() == "" or self.entry4.get() == "":
            messagebox.showerror("Error", "Complete todos los campos", parent=self.root)
        elif self.entry2.get() != self.entry4.get():
            messagebox.showerror("Error", "Contraseñas no coinciden", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="login")
                cur = con.cursor()
                cur.execute("select * from logintbl where emailid=%s", self.entry3.get())
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Usuario ya existe", parent=self.root)
                    self.regclear()
                    self.entry.focus()
                else:
                    cur.execute("INSERT INTO logintbl VALUES (%s, %s, %s, %s)",
                                (self.entry.get(), self.entry3.get(), self.entry2.get(), self.entry4.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Éxito!", "Registro completado!", parent=self.root)
                    self.regclear()
            except Exception as es:
                messagebox.showerror("Error", f"Error due to:{str(es)}", parent=self.root)

    def appscreen(self):
        self.root.withdraw()  # Close the login window
        root2 = Toplevel()  # Create a new window for the scanner and encrypt pages
        root2.title("Hoved Kit")
        root2.geometry("1366x700+0+0")
        root2.resizable(False, False)
        root2.configure(bg='#000000')

        background_img = ImageTk.PhotoImage(file="background-4.png")
        background_label = Label(root2, image=background_img)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        btn_scanner = Button(root2, text="Scanner", command=self.open_scanner, cursor="hand2",
                             font=("courier", 15),
                             bd=0, width=15, height=1, bg='#000000', fg="cyan")
        btn_scanner.place(x=500, y=500, width=200, height=50)

        btn_encrypt = Button(root2, text="Encrypt", command=self.open_encrypt, cursor="hand2",
                             font=("courier", 15),
                             bd=0, width=15, height=1, bg='#000000', fg="cyan")
        btn_encrypt.place(x=700, y=500, width=200, height=50)


        root2.mainloop()




    def open_scanner(self):
        import scanner
        scanner.startScan()
        scanner.saveScan()
        scanner.clearScan()
        scanner.updateResult()
        scanner.listScans()
        scanner.closeScanner()





    def open_encrypt(self):
        import encrypt
        encrypt.clear()
        encrypt.encrypt()
        encrypt.decrypt()
        encrypt.openUpdateWindow()
        encrypt.listEncryptions()




root = Tk()
ob = Login(root)
root.mainloop()
