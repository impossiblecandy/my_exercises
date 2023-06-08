import socket, sys, threading, time
from tkinter import *
import pymysql
from PIL import Image, ImageTk


# ==== Scan Vars ====
ip_s = 1
ip_f = 10240
log = []
ports = []
target = 'localhost'

# ==== Scanning Functions ====
def scanPort(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        c = s.connect_ex((target, port))
        if c == 0:
            m = ' Port %d \t[open]' % (port,)
            log.append(m)
            ports.append(port)
            listbox.insert("end", str(m))
            updateResult()
            # Save the scan result to the MySQL database
            con = pymysql.connect(host="localhost", user="root", password="", database="login")
            cur = con.cursor()
            cur.execute("INSERT INTO scan_results (target, port) VALUES (%s, %s)", (target, port))
            con.commit()
            con.close()

        # Your existing code here...

    except OSError:
        print('> Too many open sockets. Port ' + str(port))
    except Exception as e:
        print(str(e))
        sys.exit()




def updateResult():
    rtext = " [ " + str(len(ports)) + " / " + str(ip_f) + " ] ~ " + str(target)
    L27.configure(text=rtext)


def startScan():
    global ports, log, target, ip_f
    clearScan()
    log = []
    ports = []
    # Get ports ranges from GUI
    ip_s = int(L24.get())
    ip_f = int(L25.get())
    # Start writing the log file
    log.append('> Port Scanner')
    log.append('=' * 14 + '\n')
    log.append(' Target:\t' + str(target))

    try:
        target = socket.gethostbyname(str(L22.get()))
        log.append(' IP Adr.:\t' + str(target))
        log.append(' Ports: \t[ ' + str(ip_s) + ' / ' + str(ip_f) + ' ]')
        log.append('\n')
        # Lets start scanning ports!
        while ip_s <= ip_f:
            try:
                scan = threading.Thread(target=scanPort, args=(target, ip_s))
                scan.setDaemon(True)
                scan.start()
            except:
                time.sleep(0.01)
            ip_s += 1
    except:
        m = '> Target ' + str(L22.get()) + ' not found.'
        log.append(m)
        listbox.insert(0, str(m))

def listScans():
    try:
        con = pymysql.connect(host="localhost", user="root", password="", database="login")
        cur = con.cursor()
        cur.execute("SELECT target, port FROM scan_results")
        results = cur.fetchall()
        con.close()

        listbox.delete(0, 'end')
        for result in results:
            target = result[0]
            port = result[1]
            m = f"Target: {target} - Port: {port}"
            listbox.insert("end", str(m))
    except Exception as e:
        print(str(e))
        sys.exit()

def saveScan():
    global log, target, ports, ip_f
    log[5] = " Result:\t[ " + str(len(ports)) + " / " + str(ip_f) + " ]\n"
    with open('portscan-' + str(target) + '.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(log))


def clearScan():
    listbox.delete(0, 'end')


def closeScanner():
    global gui
    if gui is not None:
        gui.destroy()
        gui = None



# ==== GUI ====
gui = Toplevel()
gui.title('Port Scanner')
gui.geometry("800x450")
screen_width = gui.winfo_screenwidth()
screen_height = gui.winfo_screenheight()
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (450 // 2)
gui.geometry(f"800x450+{x}+{y}")


image = Image.open("background-3.png")  # Replace "splash_image.png" with the path to your image
image = image.resize((800, 450))
photo = ImageTk.PhotoImage(image)

# Set Label with image as background
gui_label = Label(gui, image=photo)
gui_label.place(x=0, y=0, relwidth=1, relheight=1)

# ==== Colors ====
m1c = 'cyan'
bgc = '#000000'
dbg = '#111111'
fgc = '#000000'

gui.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc, highlightColor=m1c,
                  highlightBackground=bgc)


# ==== Labels ====
L11 = Label(gui, text="Port Scanner", font=("Courier", 20, 'underline'))
L11.place(x=16, y=10)

L21 = Label(gui, text="Target: ", font=("Courier", 16))
L21.place(x=16, y=65)

L22 = Entry(gui, text="localhost", font=("Courier", 16))
L22.place(x=180, y=65)
L22.insert(0, "localhost")

L23 = Label(gui, text="Ports: ", font=("Courier", 16))
L23.place(x=16, y=120)

L24 = Entry(gui, text="1", font=("Courier", 16))
L24.place(x=180, y=120, width=95)
L24.insert(0, "1")

L25 = Entry(gui, text="10240", font=("Courier", 16))
L25.place(x=290, y=120, width=95)
L25.insert(0, "10240")

L26 = Label(gui, text="Results: ", font=("Courier", 16))
L26.place(x=16, y=170)
L27 = Label(gui, text="[ ... ]", font=("Courier", 16))
L27.place(x=180, y=170)

# ==== Ports list ====
frame = Frame(gui)
frame.place(x=300, y=215, width=370, height=215)
listbox = Listbox(frame, width=59, height=6)
listbox.place(x=0, y=0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# ==== Buttons / Scans ====
B11 = Button(gui, text="Scan", command=startScan, font=("Courier", 16))
B11.place(x=180, y=235, width=100)
B21 = Button(gui, text="Save", command=saveScan, font=("Courier", 16))
B21.place(x=180, y=270, width=100)
B31 = Button(gui, text="List", command=listScans, font=("Courier", 16))
B31.place(x=180, y=300, width=100)
B41 = Button(gui, text="Close", command=closeScanner, font=("Courier", 16))
B41.place(x=180, y=330, width=100)

# ==== Start GUI ====


gui.mainloop()
