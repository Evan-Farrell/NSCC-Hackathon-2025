# ==============================================================================
# Title:        guiOverlay.py
# Author:       Brad Steele
# Date:         Jan 17, 2025
# Description:  This script obtains data from backend scripts, renders a GUI,
# and allows user to update fields based on obtained data.  
# ==============================================================================

import tkinter as tk
from tkinter import *
from tkinter import filedialog, ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os
import backend

#widget layout constants
ROW_SPACING = 24.5
COMBOBOX_OFFSET = 105
WEIGHT_LABEL_OFFSET = 325
MAX_COURSES_PER_TERM = 6

#prompts filesystem dialog box, returns path to file
def searchFile():
    pwd = os.getcwd()
    return filedialog.askopenfilename(parent=root, initialdir=pwd, title='Please select a file', 
                                       filetypes=(('Excel Spreadsheet', '*.xlsx'), ("All files", "*.*")))

#prompts filesystem dialog box, returns path to directory
def searchFolder():
    pwd = os.getcwd()
    return filedialog.askdirectory(parent=root, initialdir=pwd, title='Please select a directory')

#prompts for student ID
def searchStudentID():
    return simpledialog.askstring("Student Search", "Please Input Student ID:")

#calls the function to generate populated pdf
def exportPathwayPdf():
    loading = ttk.Progressbar(root, orient='horizontal', length=200, mode='indeterminate')
    loading.place(relx=0.5, rely=0.5, anchor=CENTER)
    loading.start()
    #
    try:
        if backend.gen_pdf(value_store, header_data) == 1:
            loading.stop()
            loading.destroy()
            messagebox.showinfo("Export Success", "The PDF has been successfully exported.")
    except Exception as e:
        loading.stop()
        loading.destroy()
        messagebox.showerror("Export Error", f"Failed to export PDF: {e}")
    # finally:
    #     loading.stop()
    #     loading.destroy()

#seperates document header information and roadmap image from bulk data 
def processData(data):
    return {
        'id': data.get('id'),
        'name': data.get('name'),
        'program': data.get('program'),
        'on_track': data.get('on_track'),
        'terms_left': data.get('terms_left'),
        'progress_roadmap': data.get('progress_roadmap')
    }

#updates labels with associated course ID key 
def updateFields(combobox, label1, label2, course_data, term_key, combo_key):
    def handler(event):
        selected_code = combobox.get()
        for course in course_data:
            if course["code"] == selected_code:
                label1.config(text=course["name"])
                label2.config(text=course["unit_value"])
                value_store[term_key][combo_key] = {
                    "combobox_value": selected_code,
                    "label1_value": course["name"],
                    "label2_value": course["unit_value"]
                }
                break
    combobox.bind("<<ComboboxSelected>>", handler)

#renders widgets over background
def createWidgets(x, y, term_key, combo_index, course_data):
    combo_key = f"combobox_{combo_index + 1}"

    combobox = ttk.Combobox(root, values=[c["code"] for c in course_data], width=13)
    combobox.place(x=x, y=y + (combo_index * ROW_SPACING))

    label1 = tk.Label(root, width=30, anchor="w", bg="white", relief="solid")
    label1.place(x=x + COMBOBOX_OFFSET, y=y + (combo_index * ROW_SPACING))

    label2 = tk.Label(root, width=5, anchor="w", bg="white", relief="solid")
    label2.place(x=x + WEIGHT_LABEL_OFFSET, y=y + (combo_index * ROW_SPACING))

    value_store[term_key][combo_key] = {
        "combobox_value": None,
        "label1_value": None,
        "label2_value": None
    }

    updateFields(combobox, label1, label2, course_data, term_key, combo_key)

#initialize application
root = tk.Tk()
root.title('Student RoadmApp')
root.geometry("1594x1080")  # Size of A4 paper at 96 PPI

#retrieve data from backend
backend.parse_maps_directory(searchFolder())
backend.load_student_data(searchFile())
data = backend.get_student_info(searchStudentID())

# MAP_DIR = os.getcwd() + r'\maps\22-23'
# DATA_PATH = os.getcwd() + r"\maps\sampleData.xlsx"

# backend.parse_maps_directory(MAP_DIR)
# backend.load_student_data(DATA_PATH)
# data = backend.get_student_info('W1672629')


global header_data
header_data = processData(data)

#render background image and heatmap image
image_path = os.getcwd() + r"\resources\gui_bg_template.png"
form_image = tk.PhotoImage(file=image_path)

heatmap = header_data['progress_roadmap']
heatmap = heatmap.resize((850, 850), Image.LANCZOS)
heatmap_image = ImageTk.PhotoImage(heatmap)

template_bg = tk.Label(root, image=form_image)
heatmap_bg = tk.Label(root, image=heatmap_image)
template_bg.place(x=0, y=0)  
heatmap_bg.place(x=794, y=0)  

positions = [
    (29, 208),
    (402, 208),
    (29, 500),
    (402, 500),
    (29, 792),
    (402, 792),
]

#document header information
student_name = ttk.Label(root, text=header_data["name"], width=26)
student_name.place(x=129, y=84)
student_id = ttk.Label(root, text=header_data["id"], width=26)
student_id.place(x=554, y=84)
student_course = ttk.Label(root, text=header_data["program"], width=26)
student_course.place(x=96, y=118)

# Initialize value store
global value_store
value_store = {}

#create widgets based on number of semesters left
for term_index, (x, y) in enumerate(positions):
    if term_index >= len(data["remaining_courses"]):
        break

    term = data["remaining_courses"][term_index]
    course_list = term["course_list"]

    term_key = f"term_widget_group_{term_index + 1}"
    value_store[term_key] = {}

    for combo_index in range(MAX_COURSES_PER_TERM):
        if combo_index >= len(course_list):
            break

        createWidgets(x, y, term_key, combo_index, course_list)

# Add menu bar
menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Export to .pdf', command=exportPathwayPdf)
file_menu.add_separator()
file_menu.add_command(label='Exit Application', command=root.destroy)
root.config(menu=menubar)

# Start application
root.mainloop()
print("Exited")