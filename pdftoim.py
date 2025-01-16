import fitz
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import defaultdict
from PIL import Image
import cv2
import pandas as pd
import re
import numpy as np
import os
import time
import textwrap
from difflib import SequenceMatcher

#for testing
PDF_PATH = os.getcwd() + r"\maps\22-23\Business Intelligence Analytics - Advising Map - '22-'23.pdf"
MAP_DIR = os.getcwd() + r"\maps\22-23"
DATA_PATH= os.getcwd() + r"\SampleData\Template Data.xlsx"

LOGGING = 0



#use fitz to open the pdf
def get_nparray_from_pdf(path):
    doc = fitz.open(path)

    page = doc[0]
    pix = page.get_pixmap(dpi=500)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    return cv_image

def pdf_coord_to_png(x0_pdf, x1_pdf, y0_pdf, y1_pdf, image, page):
    width_png, height_png = image.shape[1], image.shape[0]
    width_pdf, height_pdf = page.rect.width, page.rect.height  # Example PDF size (A4 in points, 8.5"x11" at 72 DPI)

    #calculate scaling factors
    scale_x = width_png / width_pdf
    scale_y = height_png / height_pdf

    x0_png = round(x0_pdf * scale_x)
    y0_png = round((y0_pdf * scale_y))
    x1_png = round(x1_pdf * scale_x)
    y1_png = round((y1_pdf * scale_y))

    return x0_png, x1_png, y0_png, y1_png


def png_to_pdf_coord(x0_png, x1_png, y0_png, y1_png, image, page):
    width_png, height_png = image.shape[1], image.shape[0]
    width_pdf, height_pdf = page.rect.width, page.rect.height

    #calculate scaling factors
    scale_x = width_pdf / width_png
    scale_y = height_pdf / height_png

    x0_pdf = round(x0_png * scale_x)
    y0_pdf = round(y0_png * scale_y)
    x1_pdf = round(x1_png * scale_x)
    y1_pdf = round(y1_png * scale_y)

    return x0_pdf, x1_pdf, y0_pdf, y1_pdf


def log_image(name, image):
    if LOGGING:
        cv2.imwrite(os.getcwd() + "\\imgLogs\\" + name, image)


def check_if_inside(recA, recB):
    #print(f"comparing {recA} and {recB}")
    #recA
    xA0 = recA['x']
    yA0 = recA['y']
    xA1 = recA['x'] + recA['w']
    yA1 = recA['y'] + recA['h']

    #recB
    xB0 = recB['x']
    yB0 = recB['y']
    xB1 = recB['x'] + recB['w']
    yB1 = recB['y'] + recB['h']

    #check if each point in A is inside B
    if xA0 >= xB0 and yA0 >= yB0 and xA1 < xB1 and yA1 <= yB1:
        return True
    return False


def parse_map(path, count):
    image = get_nparray_from_pdf(path)
    output_image = image.copy()

    doc = fitz.open(path)
    page = doc[0]

    #define the colour range to look in
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([200, 200, 200])
    ranged_image = cv2.inRange(image, lower_black, upper_black)

    log_image(f"testranged{count}.png", ranged_image)

    # edge detection
    edges = cv2.Canny(ranged_image, 60, 80)
    kernel = np.ones((5, 5), np.uint8)

    #then dilate them to make them larger
    dilated_edges = cv2.dilate(edges, kernel, iterations=4)

    #we then want to find the two top-leftmost occurrences of the word term!
    term_recs = page.search_for("term")
    sorted(term_recs, key=lambda x: x[0])
    sorted(term_recs, key=lambda y: y[0])
    term_recs = [term_recs[0], term_recs[1]]
    term_centers = []
    for i in range(0, len(term_recs)):
        x0 = round(term_recs[i].x0)
        x1 = round(term_recs[i].x1)
        y0 = round(term_recs[i].y0)
        y1 = round(term_recs[i].y1)

        x0, x1, y0, y1 = pdf_coord_to_png(x0, x1, y0, y1, image, page)
        w = x1 - x0
        h = y1 - y0

        #this just draws a little lump where the bounding rec would be
        #crop = image[y:y + h, x:x + w]
        #cv2.rectangle(image, (x0, y0), (x0 + w, y0 + h), (255, 255, 0), 88)
        #log_image(f"boundLogs/term.png", image)

        #what we really care about here is the x value of the center
        center_x = round((x0 + x1) / 2)
        term_centers.append({'term': i + 1, 'x': center_x, 'y': y1})

        #just for visuals
        cv2.line(output_image, (center_x, y1), (center_x, image.shape[0]), (0, 255, 0), 4)

    #display the intersect lines
    log_image(f"intersectLogs/term{count}.png", output_image)

    #display the dilated edges
    log_image(f"testedges{count}.png", dilated_edges)  # Debugging: Show edges

    #find contours
    contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for contour in contours:
        #bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)

        #get rid of bound boxes above the term blocks
        if y < term_centers[0]['y']:
            continue

        #get rid of bound boxes not intersecting a term block
        #term I
        if x < term_centers[0]['x'] < x + w:
            term = 1
        #term II
        elif x < term_centers[1]['x'] < x + w:
            term = 2
        else:
            continue

        boxes.append({'x': x, 'y': y, "w": w, "h": h, "term": term})

    #now we want to eliminate "nested" boxes
    #this can be done with contour heirarchies but i was having difficulty with that...
    to_remove = []
    for boxA in boxes:
        for boxB in boxes:
            if check_if_inside(boxA, boxB):
                to_remove.append(boxA)
                #print(f"{boxA} inside {boxB}")
                break
    for box in to_remove:
        boxes.remove(box)

    if LOGGING:
        bound_count = 0
        for box in boxes:
            if box['term'] == 1:
                colour = (224, 13, 224)
            else:
                colour = (13, 34, 224)
            #must be a nicer way to unpack these
            x = box['x']
            y = box['y']
            w = box['w']
            h = box['h']

            crop = image[y:y + h, x:x + w]
            cv2.rectangle(output_image, (x, y), (x + w, y + h), colour, 7)
            log_image(f"boundLogs/bound{bound_count}.png", crop)
            bound_count = bound_count + 1

    #convert the boxes to pdf format for pyMuPDF
    pdf_bounding_boxes = []
    for box in boxes:
        x0 = box['x']
        y0 = box['y']
        x1 = x0 + box['w']
        y1 = y0 + box['h']
        pdf_box = png_to_pdf_coord(x0, x1, y0, y1, image, page)
        pdf_bounding_box = {'term': box['term'], "x0": pdf_box[0], "y0": pdf_box[2], "x1": pdf_box[1], "y1": pdf_box[3]}
        pdf_bounding_boxes.append(pdf_bounding_box)
        #print(f"converted {box} to {pdf_box}")

    log_image(f"testbounded{count}.png", output_image)

    return (pdf_bounding_boxes)
    #IN THE FUTURE THIS CAN BE EXPANDED TO POSSIBLY GATHER PREREQS...


#gives similarity of two strings, to account for typos in the pdf names
def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def parse_maps_directory(dir):
    programs = defaultdict(dict)

    #check errors check errors check erros >:(
    for pdf in os.listdir(dir):
        if os.path.splitext(pdf)[1] != '.pdf':
            continue

        #check that it's actually a pdf blah bloah blah

        #split the title
        pdf_arr = pdf.split('-')

        #get the title, spell check it... some of the pdfs were not spelled the same >:(
        programTitle = pdf_arr[0].strip()
        for program in programs.keys():
            similarity = string_similarity(programTitle, program)
            if similarity > 0.9:
                # print(f"{program} and {programTitle} have {similarity}")
                programTitle = program

        #check for year/if it is a 2-year program
        if "year1" in pdf.lower().replace(" ", ""):
            programs[programTitle]['year1'] = dir + "\\" + pdf
        elif "year2" in pdf.lower().replace(" ", ""):
            programs[programTitle]['year2'] = dir + "\\" + pdf
        else:
            programs[programTitle]['year0'] = dir + "\\" + pdf

    return (programs)


def parse_boxes(boxes, path, program,year):
    doc = fitz.open(path)
    page = doc[0]

    #Finds strings that match the AAAA 1234 class code pattern
    class_pattern = r"\b[A-Z]{4}\s\d{4}\b"

    class_list=[]
    for box in boxes:
        x0 = box['x0']
        y0 = box['y0']
        x1 = box['x1']
        y1 = box['y1']

        look_area = (x0, y0, x1, y1)
        text = page.get_textbox(look_area)


        #first check if it contains a class code
        searched = re.findall(class_pattern, text)
        #if the search is empty check it might be an elective
        if len(searched)==0:
            if "elective" in text.lower():
                class_to_add = {"name":"Elective",
                      "code":"ELEC",
                      "term":box['term'],
                      "unit_value":"PLACEHOLD",
                      "program": program,
                      "year":year}
                class_list.append(class_to_add)
                continue

            else:
                #found nothing of value:c
                continue
        class_code=searched[0]
        class_name=text[0:text.index(class_code)].replace("\n","")

        #if the class name is empty but we found a code it means there was an errant box
        #this happens on the pdfs that are premarked (IT Data Analytics 22-23 year 2 for example)
        if not class_name:
            continue

        class_to_add={"name":class_name,
                      "code":class_code,
                      "term":box['term'],
                      "unit_value":"PLACEHOLD",
                      "program": program,
                      "year":year}
        class_list.append(class_to_add)
    return class_list


def parse_programs(programs):
    global CLASS_DATAFRAME
    count = 0
    class_list=[]
    for program in programs.keys():
        for term in programs[program].keys():
            bound_boxes = parse_map(programs[program][term], count)
            #append this maps classes to the classlist array
            class_list=class_list + parse_boxes(bound_boxes, programs[program][term], program,term)


            count += 1


    CLASS_DATAFRAME=pd.DataFrame.from_dict(class_list)
    CLASS_DATAFRAME.to_csv("test.csv",index=False)

    print(CLASS_DATAFRAME)

def load_student_data(path):
    global STUDENT_DATAFRAME
    STUDENT_DATAFRAME=pd.read_excel(DATA_PATH, engine='openpyxl')


    #first we want to map the weird abbreivations to something more readable
    #i.e ITDBADMIN -> IT Database Administration
    abbreviations=STUDENT_DATAFRAME['Acad Plan'].unique()
    program_names = CLASS_DATAFRAME['program'].unique()

    for abbrev in abbreviations:
        #get all the classes a student in a certain abbreviation took
        prog_df=STUDENT_DATAFRAME[STUDENT_DATAFRAME['Acad Plan'] == abbrev]
        abbrevs_classes=prog_df['Subject']+" "+prog_df['Catalog']

        #get the program that shares the most overlap with the courses
        overlap=CLASS_DATAFRAME[CLASS_DATAFRAME['code'].isin(abbrevs_classes)]
        best_guess=overlap['program'].value_counts().idxmax()

        # print(f"{abbrev} means {best_guess} with {overlap['program'].value_counts()[0]} overlap")

        #if the overlap is very little dont say anything with certainty!
        if overlap['program'].value_counts()[0] > 5:
            STUDENT_DATAFRAME['Acad Plan'] = STUDENT_DATAFRAME['Acad Plan'].replace(abbrev, best_guess)
        else:
            STUDENT_DATAFRAME['Acad Plan'] = STUDENT_DATAFRAME['Acad Plan'].replace(abbrev, best_guess)

    #then combine the subject+catlog into one cell
    STUDENT_DATAFRAME['code'] = STUDENT_DATAFRAME['Subject'] + ' ' + STUDENT_DATAFRAME['Catalog']

def get_student_info(id):

    courses_taken=STUDENT_DATAFRAME[STUDENT_DATAFRAME['Empl ID']==id]
    student_name=courses_taken['Student Name'].values[0]
    student_program=courses_taken['Acad Plan'].values[0]
    # print(student_program)

    classes_needed=CLASS_DATAFRAME[CLASS_DATAFRAME['program']==student_program].copy()
    classes_needed['attempted'] ="unknown"
    classes_needed['passed'] = "unknown"

    #check which classes they passed
    #ASK WHAT A GRADE OF I MEANS
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

    #now break the courses into year and term

    #make graph
    make_student_graph(classes_needed.copy(),student_name,id)
    return
    #make plan
    num_years=len(classes_needed['year'].unique())
    credits_passed=len(classes_needed[classes_needed['passed']==1])
    print(credits_passed)
    terms=[]*num_years
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

start=time.time()

# programs = parse_maps_directory(MAP_DIR)
# parse_programs(programs)
pd.options.display.max_columns = 100
CLASS_DATAFRAME=pd.read_csv("test.csv")
load_student_data(DATA_PATH)

get_student_info(1672787)
# for x in range(0,100):
#     get_student_info(1672629)
# get_student_info(1672629)
#failed twice
# get_student_info(1635643)
print(f"took {time.time() - start} secs")

# make_student_graph("foo")
# Sample data: courses and their statuses


