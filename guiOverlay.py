import tkinter
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

def filterTermInfo(studentData):
    courses_per_term = []
    for i in range(0,len(studentData['remaining_courses'])):
        for course in studentData['remaining_courses'][i]['course_list']:
            courses_per_term.append(course)

    return courses_per_term

def createCourselist(root, codes):
    sessionCombos = []
    possible_codes=[]

    for course in codes:
        possible_codes.append(course['code'])

    for i in range(6):
        var_store = Variable()
        course_id = ttk.Combobox(root, textvariable=var_store, width=9)
        course_id['values'] = possible_codes
        course_id.state(["readonly"])
        sessionCombos.append(course_id)

    return sessionCombos

def placeTermCourse(courseList, bg):
    for i in range(6):
        courseList[i].place(x=57, y=(225 + (i * 20)))
        courseList[i].tkraise(aboveThis=bg)



# info_test = {'id': 'W0518150', 'name': 'Evan Farrell', 'program': 'iot blah blah', 'on_track': 1, 'terms_left': 2, 'progress_roadmap': 'some image file.png', 'remaining_courses': [{'term_session': 'Fall 2019', 'course_list': [{'name': 'widgets 101', 
# 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}, {'term_session': 'Winter 2020', 'course_list': [{'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}, {'name': 'widgets 101', 'code': 'W1000', 'unit_value': 1, 'misc': 'could add anything else you need...'}]}]}

# filterTermInfo(info_test)
# exit()


root = tkinter.Tk()
root.title('Student RoadmApp')
root.geometry("794x1123") #size of A4 paper at 96PPI
#root.withdraw() #use to hide tkinter window

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

coursevar = filterTermInfo(info_test)
#print(coursevar)
term_courseList = createCourselist(root, coursevar[0:6])


#background image rendering (change path later)
image = PhotoImage(file="overlay-test.png")

template_bg = Label(root, image=image)
template_bg.place(x=0, y=0)

placeTermCourse(term_courseList, template_bg)

root.config(menu=menubar)
root.mainloop()

# for testing dialog functions
#folderLoc = searchFolder()
#print(folderLoc)

#fileLoc = searchFile()
#print(fileLoc)
