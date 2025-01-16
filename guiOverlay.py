import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os

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


# info_test = {'id': 'W0518150', 'name': 'Evan Farrell', 'program': 'iot blah blah', 'on_track': 1, 'terms_left': 2, 'progress_roadmap': 'some image file.png', 'remaining_courses': [{'term_session': 'Fall 2019', 'course_list': [{'name': 'widgets 101', 
# 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}]}

# filterTermInfo(info_test)
# exit()


root = tk.Tk()
root.title('Student RoadmApp')
root.geometry("794x1123") #size of A4 paper at 96PPI
#root.withdraw() #use to hide tkinter window

# Load the background image
image = tk.PhotoImage(file="overlay-test.png")
template_bg = tk.Label(root, image=image)
template_bg.place(x=0, y=0)  # Position the image at the top-left corner

# Define values for each ComboBox
combo_values = [
    ["Option 1", "Option 2", "Option 3"],
    ["One", "Two", "Three", "Four"],
    ["A", "B", "C"],
    ["Alpha", "Beta"],
    ["Red", "Green", "Blue", "Yellow"],
    ["January", "February", "March", "April", "May", "June"],
]

# Define positions for the widget groups
positions = [
    (0, 0),   # Top-left
    (397, 0),  # Top-right
    (0, 373),  # Middle-left
    (397, 373),  # Middle-right
    (0, 746),  # Bottom-left
    (397, 746),  # Bottom-right
]

def update_label(combobox, label):
    """Update the labels based on the combobox selection."""
    label.config(text=combobox.get())

# Create and position the widgets directly
for i, (x, y) in enumerate(positions):
    for j in range(6):  # Each position has 6 sets of widgets
        # Create the ComboBox
        values = combo_values[j % len(combo_values)]  # Varying values for ComboBoxes
        combobox = ttk.Combobox(root, values=values, width=9)
        combobox.place(x=x, y=y + (j * 20))

        # Create the first Label (27 pixels wide equivalent)
        label1 = tk.Label(root, width=27, anchor="w", bg="white", relief="solid")
        label1.place(x=x + 77, y=y + (j * 20))  # Positioned tightly to the right of the ComboBox

        # Create the second Label (6 pixels wide equivalent)
        label2 = tk.Label(root, width=6, anchor="w", bg="white", relief="solid")
        label2.place(x=x + 233, y=y + (j * 20))  # Positioned tightly to the right of the first Label

        # Bind the ComboBox to update the first Label
        combobox.bind("<<ComboboxSelected>>", lambda event, c=combobox, l=label1: update_label(c, l))
        combobox.bind("<<ComboboxSelected>>", lambda event, c=combobox, l=label2: update_label(c, l), add='+')

        # Update the second Label whenever the first Label changes
        # label1.bind("<Configure>", lambda event, l1=label1, l2=label2: update_label2(l1, l2))


#adds a dropdown menu in window (still need to implement function calls)
menubar = Menu(root)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Select Data Source', command=searchFile)
file_menu.add_command(label='Select Roadmap Directory', command=searchFolder)
file_menu.add_separator()
file_menu.add_command(label='Exit Application', command=root.destroy)

info_test = {'id': 'W0518150', 'name': 'Evan Farrell', 'program': 'iot blah blah', 'on_track': 1, 'terms_left': 2, 'progress_roadmap': 'some image file.png', 'remaining_courses': [{'term_session': 'Fall 2019', 'course_list': [{'name': 'widgets 101', 
'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}]}




root.config(menu=menubar)
# Start the application
root.mainloop()