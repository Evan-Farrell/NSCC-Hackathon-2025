import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

def searchFile():
    pwd = os.getcwd()
    fileLocation = filedialog.askopenfilename(parent=root, initialdir=pwd, title='Please select a file', filetypes=(('Excel Spreadsheet', '*.xlsx'), ("All files", "*.*")))
    return fileLocation

def searchFolder():
    pwd = os.getcwd()
    directoryLoc = filedialog.askdirectory(parent=root, initialdir=pwd, title='Please select a directory')
    return directoryLoc

#folderLoc = searchFolder()
#print(folderLoc)

fileLoc = searchFile()
print(fileLoc)