from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image


# Create object
splash_root = Tk()
splash_root.title("Heimdall Sec.")
# Adjust size
splash_root.geometry("800x450")

# Calculate the screen's width and height
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()

# Calculate the coordinates to center the splash screen
x = (screen_width // 2) - (800 // 2)
y = (screen_height // 2) - (450 // 2)

# Set the splash screen to open in the center of the screen
splash_root.geometry(f"800x450+{x}+{y}")

# Load image
image = Image.open("Picture1.png")
image = image.resize((800, 450))
photo = ImageTk.PhotoImage(image)

# Set Label with image as background
splash_label = Label(splash_root, image=photo)
splash_label.place(x=0, y=0, relwidth=1, relheight=1)

# Progress bar
style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar",
                background='black',
                troughcolor='white',
                troughrelief='flat',
                bordercolor='black',
                lightcolor='black',
                darkcolor='black',
                thickness=10)
progress = Progressbar(splash_root, style="black.Horizontal.TProgressbar",
                       orient=HORIZONTAL, length=800, mode='determinate')
progress.place(x=0, y=430, relwidth=1)

# main window function
def main():
    # Destroy splash window
    splash_root.destroy()
    import login
    login()
# Function to update progress bar
def update_progress():
    for i in range(4):  # Update the range according to the duration (3 seconds)
        progress['value'] = i * 25
        splash_root.update_idletasks()
        splash_root.after(750)  # Update the progress bar every 750 milliseconds (0.75 seconds)

    main() # Call the main window function after the progress bar completes

# Set Interval
splash_root.after(1000, update_progress)  # Start updating the progress bar after 1 second

# Execute tkinter
mainloop()


