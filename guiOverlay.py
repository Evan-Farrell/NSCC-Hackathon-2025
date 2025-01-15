import tkinter
from tkinter import *
from tkinter import filedialog
import os

root = tkinter.Tk()
root.title('Student RoadmApp')
root.geometry("817x1027") #size of template image
#root.withdraw() #use to hide tkinter window

#adds a dropdown menu in window (still need to implement function calls)
menubar = Menu(root)

fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=fileMenu)
fileMenu.add_command(label='Select Data Source', command=None)
fileMenu.add_command(label='Select Roadmap Directory', command=None)
fileMenu.add_separator()
fileMenu.add_command(label='Exit Application', command=root.destroy)

#background image rendering (change path later)
image = PhotoImage(file="overlay-test.png")

canvas1 = Canvas(root, width=817, height=1027)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=image, anchor="nw")


#prompts filesystem dialog box, returns path to file
def searchFile():
    pwd = os.getcwd()
    fileLocation = filedialog.askopenfilename(parent=root, initialdir=pwd, title='Please select a file', filetypes=(('Excel Spreadsheet', '*.xlsx'), ("All files", "*.*")))
    return fileLocation

#prompts filesystem dialog box, returns path to directory
def searchFolder():
    pwd = os.getcwd()
    directoryLoc = filedialog.askdirectory(parent=root, initialdir=pwd, title='Please select a directory')
    return directoryLoc


root.config(menu=menubar)
root.mainloop()

# for testing dialog functions
#folderLoc = searchFolder()
#print(folderLoc)

#fileLoc = searchFile()
#print(fileLoc)
