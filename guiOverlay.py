import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
import os
import backend

#prompts filesystem dialog box, returns path to file
def searchFile():
    pwd = os.getcwd()
    file_path = filedialog.askopenfilename(parent=root, initialdir=pwd, title='Please select a file', filetypes=(('Excel Spreadsheet', '*.xlsx'), ("All files", "*.*")))
    return file_path


#prompts filesystem dialog box, returns path to directory
def searchFolder():
    pwd = os.getcwd() 
    directory_path = filedialog.askdirectory(parent=root, initialdir=pwd, title='Please select a directory')
    return directory_path

def searchStudentID():
    student_id = simpledialog.askstring("Student Search", "Please Input Student ID:")
    #student_id="W1635643"
    return student_id

def exportPathwayPdf(completed_values):
    loading = ttk.Progressbar(root, orient='horizontal', length=18, mode='indeterminate')
    loading.start()
    if (backend.gen_pdf(completed_values) == 1):
        loading.stop()
    return

#accepts data object pulled from spreadsheet, returns two data objects
def process_data(data):
    #extract top level info
    top_level_info = {
        'id': data.get('id'),
        'name': data.get('name'),
        'program': data.get('program'),
        'on_track': data.get('on_track'),
        'terms_left': data.get('terms_left'),
        'progress_roadmap': data.get('progress_roadmap'),
    }
    #extract and pack each term
    # remaining_courses = {}
    # for term in data.get('remaining_courses', []):
    #     term_session = term.get('term_session')
    #     course_list = term.get('course_list', [])

    #     #format the course list for clarity
    #     remaining_courses[term_session] = [
    #         {
    #             'name': course.get('name'),
    #             'code': course.get('code'),
    #             'unit_value': course.get('unit_value'),
    #             'misc': course.get('misc')
    #         }
    #         for course in course_list
    #     ]
    return top_level_info #remaining_courses

#------------
# PDF_PATH = os.getcwd() + r"\maps\22-23\Business Intelligence Analytics - Advising Map - '22-'23.pdf"
# MAP_DIR = os.getcwd() + r"\maps\22-23"
#DATA_PATH= os.getcwd() + r"\SampleData\Template Data.xlsx"
#backend.parse_maps_directory('1')
#backend.load_student_data(DATA_PATH)
# print(backend.get_student_info("W1635643"))
# exit()
#-----------
root = tk.Tk()
root.title('Student RoadmApp')
root.geometry("794x1123") #size of A4 paper at 96PPI
#root.withdraw() #use to hide tkinter window

backend.parse_maps_directory(searchFolder())
backend.load_student_data(searchFile())
#data=backend.get_student_info("W1635643")
data = backend.get_student_info(searchStudentID())

#load the background image
image = tk.PhotoImage(file="gui_bg_template.png")
template_bg = tk.Label(root, image=image)
template_bg.place(x=0, y=0)  #origin at top-left
#define positions for the widget groups
positions = [
    (29, 208),   # [row1][column1]
    (402, 208),  # [row1][column2]
    (29, 500),  # [row2][column1]
    (402, 500),  # [row2][column2]
    (29, 792),  # [row3][column1]
    (402, 792),  # [row3][column2]
]

# #get selected coursecode, search for matching course name and weight 
# def update_labels(event, combobox, label1, label2, course_data):
#     selected_code = combobox.get()
#     for course in course_data:
#         if course["code"] == selected_code:
#             label1.config(text=course["name"])
#             label2.config(text=course["unit_value"])
#             break
# data = {'id': 'W1635643', 'name': 'Bill Flores', 'program': 'IT Web Programming', 'on_track': 0, 'terms_left': 0, 'progress_roadmap': <PIL.Image.Image image mode=RGBA size=1500x1500 at 0x15A0CFED6D0>, 'remaining_courses': [{'term_session': 'Fall 2025', 'course_list': [{'name': 'Web Application Programming I', 'code': 'INET 2005', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'Full Stack Programming', 'code': 'PROG 3017', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'Elective', 'code': 'ELEC', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'Web Design Fundamentals', 'code': 'WEBD 3100', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'Project Management', 'code': 'INFT 2100', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'Professional Practices for IT III', 'code': 'COMM 3700', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2025', 'course_list': [{'name': 'User Interface Design & Development', 'code': 'APPD 1001', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'Client Side 
# data = {'id': 'W0518150', 'name': 'Evan Farrell', 'program': 'iot blah blah', 'on_track': 1, 'terms_left': 2, 'progress_roadmap': 'some image file.png', 'remaining_courses': [{'term_session': 'Fall 2019', 'course_list': [{'name': 'widgets 201', 
# 'code': 'W1002', 'unit_value': 1.5, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]},]}

#initialize value store
value_store = {}

#function to update labels and store the values
def update_labels(event, combobox, label1, label2, course_data, term_key, combo_key):
    selected_code = combobox.get()
    for course in course_data:
        if course["code"] == selected_code:
            #update labels
            label1.config(text=course["name"])
            label2.config(text=course["unit_value"])
            
            #update value store
            value_store[term_key][combo_key] = {
                "combobox_value": selected_code,
                "label1_value": course["name"],
                "label2_value": course["unit_value"]
            } 
            break

header_data = process_data(data)

student_name = ttk.Label(root, text=header_data["name"], width=26)
student_name.place()
student_id = ttk.Label(root, text=header_data["id"], width=26)
student_id.place()
student_course = ttk.Label(root, text=header_data["program"], width=26)
student_course.place()

#create and position widgets (3 rows, 2 columns; [row][column]order)
for term_index, (x, y) in enumerate(positions):

    if term_index >= len(data["remaining_courses"]):
        break  #if there aren't enough terms to fill all 6 tables, break loop

    term = data["remaining_courses"][term_index]
    course_list = term["course_list"]

    #create term
    term_key = f"term_widget_group_{term_index + 1}"

    #initialize nested dictionary for current term
    value_store[term_key] = {}

    for combo_index in range(6):  #maximum of 6 courses per term
        #if there's less than six courses in this term, break the loop
        if combo_index >= len(course_list):
            break

        course = course_list[combo_index]

        #create a key for this combobox
        combo_key = f"combobox_{combo_index + 1}"

        #build combobox widget, populate with values of "code" key
        combobox = ttk.Combobox(root, values=[c["code"] for c in course_list], width=13)
        combobox.place(x=x, y=y + (combo_index * 24.5))

        #build course name widget, place next to combobox
        label1 = tk.Label(root, width=30, anchor="w", bg="white", relief="solid")
        label1.place(x=x + 105, y=y + (combo_index * 24.5))

        #build course weight widget, place next to course name
        label2 = tk.Label(root, width=5, anchor="w", bg="white", relief="solid")
        label2.place(x=x + 325, y=y + (combo_index * 24.5))

        #initialize the entry in value_store for this combobox
        value_store[term_key][combo_key] = {
            "combobox_value": None,
            "label1_value": None,
            "label2_value": None
        }

        #bind the combobox to update the labels and value store on option selection
        combobox.bind(
            "<<ComboboxSelected>>",
            lambda event, c=combobox, l1=label1, l2=label2, data=course_list, tk=term_key, ck=combo_key: update_labels(event, c, l1, l2, data, tk, ck)
        )


#adds a dropdown menu in window, calls file/folder system dialog or exits app
menubar = Menu(root)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Select Data Source', command=searchFile)
file_menu.add_command(label='Select Roadmap Directory', command=searchFolder)
file_menu.add_command(label='Export to .pdf', command=exportPathwayPdf)
file_menu.add_separator()
file_menu.add_command(label='Exit Application', command=root.destroy)


root.config(menu=menubar)

#start the application
root.mainloop()