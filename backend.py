import math
import mapParsing
import studentDataParsing
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import exportPDF
import pandas as pd
import numpy as np
import os
import time
import textwrap




#for testing

FORMAT_PATH=os.getcwd()+ r"\resources\format.pdf"

LAST_SEARCHED_ID=0
STUDENT_DATAFRAME={}
CLASS_DATAFRAME={}

def parse_maps_directory(dir):
    global CLASS_DATAFRAME
    CLASS_DATAFRAME=mapParsing.parse_directory(dir)

def load_student_data(path):
    global STUDENT_DATAFRAME
    STUDENT_DATAFRAME=studentDataParsing.load_student_data(path,CLASS_DATAFRAME)

def gen_pdf(data):
    return exportPDF.gen_pdf(data)

def get_student_info(id):

    if str(id)[0].upper() =="W":
        id=int(str(id)[1:])

    courses_taken=STUDENT_DATAFRAME[STUDENT_DATAFRAME['Empl ID']==id]
    student_name=courses_taken['Student Name'].values[0]
    student_program=courses_taken['Acad Plan'].values[0]

    classes_needed=CLASS_DATAFRAME[CLASS_DATAFRAME['program']==student_program].copy()
    classes_needed['attempted'] ="unknown"
    classes_needed['passed'] = "unknown"

    #check which classes they passed
    #TODO: get electives working
    #TODO: ask what a grade of I means
    for index_need, needed_course in classes_needed.iterrows():

        needed_code=needed_course['code']
        checker=courses_taken[courses_taken['code']==needed_code]
        times_taken=checker.shape[0]
        if times_taken == 0:
            classes_needed.loc[index_need,'attempted']=0
            classes_needed.loc[index_need,'passed']=0
        elif times_taken == 1:
            grade=checker["Official Grade"].values[0]
            if grade == "W" or grade =="F" or grade =="I":
                classes_needed.loc[index_need, 'attempted'] = 1
                classes_needed.loc[index_need, 'passed'] = 0
            else:
                classes_needed.loc[index_need, 'attempted'] = 1
                classes_needed.loc[index_need, 'passed'] = 1
        else:
            grades=checker["Official Grade"].values
            marker=0
            for grade in grades:
                if grade == "W" or grade == "F" or grade == "I":
                    continue
                #if we made it here then they got a grade and passed presumably
                marker=1
            if marker:
                classes_needed.loc[index_need, 'attempted'] = 1
                classes_needed.loc[index_need, 'passed'] = 1
            else:
                classes_needed.loc[index_need, 'attempted'] = 1
                classes_needed.loc[index_need, 'passed'] = 0

        # print(f"{student_name} results for " +
        #       f"{classes_needed.loc[index_need,'name',]}" +
        #       f" PASSED: {classes_needed.loc[index_need,'passed']}" +
        #       f" ATTEMPTED: {classes_needed.loc[index_need,'attempted']}")

    #create student info for gui...
    classes_left=classes_needed[classes_needed['passed']==0]

    term1=classes_left[classes_left['term']==1]
    term2 = classes_left[classes_left['term'] == 2]

    remaining_courses = []
    num_fall_terms=math.ceil(len(term1)/6)
    num_winter_terms=math.ceil(len(term2)//6)

    add_count=0
    for term in range(0,num_fall_terms):
        course_list=[]
        while len(course_list)<=5 and add_count<len(term1):
            course = {"name": term1.iloc[add_count]['name'],
                      "code": term1.iloc[add_count]['code'],
                      "unit_value": term1.iloc[add_count]['unit_value'],
                      "misc": "could add anything else you need..."
                      }
            add_count=add_count+1
            course_list.append(course)
        term_to_add = {"term_session": f"Fall 20{25+term}",
                     "course_list": course_list
                     }
        remaining_courses.append(term_to_add)

    add_count = 0
    for term in range(0, num_winter_terms):
        course_list = []
        while len(course_list) <= 5 and add_count < len(term2):
            course = {"name": term2.iloc[add_count]['name'],
                      "code": term2.iloc[add_count]['code'],
                      "unit_value": term2.iloc[add_count]['unit_value'],
                      "misc": "could add anything else you need..."
                      }
            add_count = add_count + 1
            course_list.append(course)
        term_to_add = {"term_session": f"Winter 20{25 + term}",
                       "course_list": course_list
                       }
        remaining_courses.append(term_to_add)

    student_info = {
        'id':"W"+str(id),
        'name': student_name,
        'program': student_program,
        'on_track': 0, #placehold
        'terms_left': 0, #placehold
        'progress_roadmap': make_student_graph(classes_needed.copy(),student_name,id),
        'remaining_courses': remaining_courses
    }
    return student_info

def make_student_graph(courses,name,id):
    num_years = len(courses['year'].unique())
    counts = courses.groupby(['term', 'year']).size().reset_index(name='count')
    max_in_a_term=counts['count'].max()

    #assign colours to each class
    courses['colour'] = "unknown"
    for index_course, course in courses.iterrows():
        if course['passed'] == 1:
            courses.loc[index_course, 'colour'] = 'green'
        elif course['passed'] == 0 and course['attempted'] == 0:
            courses.loc[index_course, 'colour'] = 'yellow'
        else:
            courses.loc[index_course, 'colour'] = 'red'


    fig, ax = plt.subplots(figsize=(15, 15))

    cols = num_years * 2
    rows = max_in_a_term

    box_width = 4.5
    box_height = 4
    padding = 1

    courses=courses.sort_values(by=['year','term'])
    semesters = courses.groupby(['year', 'term'])

    #make headers
    for col in range(cols):
        x = col * (box_width + padding) + box_width / 2  # Center the header
        y = padding + box_height  # Place the header above the top row
        ax.text(x, y, f"Semester {col + 1}", ha='center', va='center', fontsize=6, weight='bold')

    #iterate per semester
    for i, (_, semester_df) in enumerate(semesters):
        for j, (_, course) in enumerate(semester_df.iterrows()):

            col = i % cols
            row = j

            x = col * (box_width + padding)
            y = -(row * (box_height + padding))

            colour = course.loc['colour']
            rect = patches.Rectangle((x, y), box_width, box_height, linewidth=1, edgecolor='black', facecolor=colour)
            ax.add_patch(rect)
            wrapped_text = textwrap.fill(course.loc['name'], width=15)

            ax.text(x + box_width / 2,
                    y + box_height / 2,
                    wrapped_text, ha='center', va='center', fontsize=10, color='black')

    ax.set_xlim(-padding, cols * (box_width + padding))
    ax.set_ylim(-(rows * (box_height + padding)), padding + 2 * box_height)
    ax.axis('off')

    plt.title(f"Academic map for {courses['program'].iloc[0]} \n {name} {id}    ")

    plt.show()

    #fig to a PIL Image
    fig.canvas.draw()
    raw_data = fig.canvas.buffer_rgba()
    width, height = fig.canvas.get_width_height()
    image_array = np.frombuffer(raw_data, dtype=np.uint8).reshape(height, width, 4)
    pil_image = Image.fromarray(image_array)
    plt.clf()

    return pil_image



if __name__ == "__main__":

    PDF_PATH = os.getcwd() + r"\maps\22-23\Business Intelligence Analytics - Advising Map - '22-'23.pdf"
    MAP_DIR = os.getcwd() + r"\maps\22-23"
    DATA_PATH = os.getcwd() + r"\maps\sampleData.xlsx"
    start=time.time()

    # CLASS_DATAFRAME = mapParsing.parse_directory(MAP_DIR)

    pd.options.display.max_columns = 100
    CLASS_DATAFRAME=pd.read_csv("resources/test.csv")
    load_student_data(DATA_PATH)

    # get_student_info("W1635643")
    # 1635643
    print(get_student_info("W1672629"))
    #failed twice
    # get_student_info(1635643)

    print(f"took {time.time() - start} secs")


