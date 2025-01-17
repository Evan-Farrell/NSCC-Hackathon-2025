# ==============================================================================
# Title:        mapParsing.py
# Author:       Evan Farrell
# Date:         Jan 17, 2025
# Description:  This script performs image processing tasks on the class roadmap PDFS with
#               edge detection contour finding, and image manipulation using OpenCV and NumPy.
# ==============================================================================

import os
from collections import defaultdict
import re
from difflib import SequenceMatcher
import cv2
import fitz
import numpy as np
import pandas as pd
from PIL import Image

LOGGING = 0
def log_image(name, image):
    """
        Saves the provided image to a file if logging is enabled.
    """
    if LOGGING:
        cv2.imwrite(os.getcwd() + "\\imgLogs\\" + name, image)

def pdf_coord_to_png(x0_pdf, x1_pdf, y0_pdf, y1_pdf, image, page):
    """
        Converts coordinates from the PDF coordinate system to the PNG coordinate system.
    """
    #get the dimensions of image and pdf
    width_png, height_png = image.shape[1], image.shape[0]
    width_pdf, height_pdf = page.rect.width, page.rect.height

    #calculate scaling factors
    scale_x = width_png / width_pdf
    scale_y = height_png / height_pdf

    x0_png = round(x0_pdf * scale_x)
    y0_png = round((y0_pdf * scale_y))
    x1_png = round(x1_pdf * scale_x)
    y1_png = round((y1_pdf * scale_y))

    return x0_png, x1_png, y0_png, y1_png

def png_to_pdf_coord(x0_png, x1_png, y0_png, y1_png, image, page):
    """
          Converts coordinates from the PNG coordinate system to the PDF coordinate system.
    """
    #get the dimensions of image and pdf
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

def parse_directory(dir):
    """
          Goes through the passed directory and maps each program title to the corresponding path
    """

    #If passed '1' just immediately return the data for front end testing
    if str(dir) == '1':
        CLASS_DATAFRAME=pd.read_csv("resources/test.csv")
        return CLASS_DATAFRAME

    programs = defaultdict(dict)

    #Skip non-pdf files
    for pdf in os.listdir(dir):
        if os.path.splitext(pdf)[1] != '.pdf':
            continue

        #split the title
        pdf_arr = pdf.split('-')

        #get the title, spell check it... some of the pdfs were not spelled the same >:(
        programTitle = pdf_arr[0].strip()
        for program in programs.keys():
            similarity = SequenceMatcher(None, programTitle, program).ratio()
            #if two titles are very similar assume they are the same program and set them equal
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

    return parse_programs(programs)

def parse_programs(programs):
    """
        For each program generating the bounding boxes for the programs 'parse_map()',
        and then parse the boxes 'parse_boxes()'
    """
    #keep a count for image logging purposes
    count = 0
    class_list=[]
    for program in programs.keys():
        for term in programs[program].keys():
            bound_boxes = parse_map(programs[program][term], count)
            class_list=class_list + parse_boxes(bound_boxes, programs[program][term], program,term)
            count += 1
        print(f"Parsed {program}")

    CLASS_DATAFRAME=pd.DataFrame.from_dict(class_list)

    #optionally save the csv for quick access for bug testing
    #CLASS_DATAFRAME.to_csv("test.csv",index=False)

    return CLASS_DATAFRAME


def parse_map(path, count):
    """
        Given the path to an academic map, perform some image analysis to create bounding boxes around the information
        we want
    """
    def check_if_inside(recA, recB):
        """
            Little helper function to check if recA is inside recB!
        """
        # recA
        xA0 = recA['x']
        yA0 = recA['y']
        xA1 = recA['x'] + recA['w']
        yA1 = recA['y'] + recA['h']

        # recB
        xB0 = recB['x']
        yB0 = recB['y']
        xB1 = recB['x'] + recB['w']
        yB1 = recB['y'] + recB['h']

        #check if each point in A is inside B
        if xA0 >= xB0 and yA0 >= yB0 and xA1 < xB1 and yA1 <= yB1:
            return True
        return False

    #convert the pdf to an image
    doc = fitz.open(path)
    page = doc[0]
    pix = page.get_pixmap(dpi=500)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    #convert image from np_array to cv2 image (they use different colour schemes)
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    output_image = image.copy()

    #define the colour range to look in (we only want to worry about colours that contain info we need)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([200, 200, 200])
    ranged_image = cv2.inRange(image, lower_black, upper_black)



    #use Canny edge detector to get just the 'edges' of things in the image
    edges = cv2.Canny(ranged_image, 60, 80)
    kernel = np.ones((5, 5), np.uint8)

    #dilate edges them to make them larger (this is to connect small gaps in the rectangles that might exist
    dilated_edges = cv2.dilate(edges, kernel, iterations=4)

    #we then want to find the two top-leftmost occurrences of the word term
    #all the rectangles representing classes are directly below a term box
    #so by checking an intersection of the x-coord of a term box we can determine what
    #class a term is in!
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

        #what we really care about here is the x value of the center
        center_x = round((x0 + x1) / 2)
        term_centers.append({'term': i + 1, 'x': center_x, 'y': y1})

        #just for visuals
        if LOGGING:
            cv2.line(output_image, (center_x, y1), (center_x, image.shape[0]), (0, 255, 0), 4)

    #find contours (this is basically a list of connected shapes from the dilated_edges image)
    contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for contour in contours:

        #create a rectangle around each contour
        x, y, w, h = cv2.boundingRect(contour)

        #get rid of bound boxes above the term blocks
        if y < term_centers[0]['y']:
            continue

        #get rid of bound boxes not intersecting a term block's x coordinate
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
    #this can be done with contour hierarchies, but I was having difficulty with that...
    to_remove = []
    for boxA in boxes:
        for boxB in boxes:
            if check_if_inside(boxA, boxB):
                to_remove.append(boxA)
                break
    for box in to_remove:
        boxes.remove(box)

    #draw all the boxes on the output image for logging
    if LOGGING:
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

            cv2.rectangle(output_image, (x, y), (x + w, y + h), colour, 7)

    #convert the boxes to pdf format for pyMuPDF to extract text
    pdf_bounding_boxes = []
    for box in boxes:
        x0 = box['x']
        y0 = box['y']
        x1 = x0 + box['w']
        y1 = y0 + box['h']
        pdf_box = png_to_pdf_coord(x0, x1, y0, y1, image, page)
        pdf_bounding_box = {'term': box['term'], "x0": pdf_box[0], "y0": pdf_box[2], "x1": pdf_box[1], "y1": pdf_box[3]}
        pdf_bounding_boxes.append(pdf_bounding_box)

    log_image(f"boundLogs/testbounded{count}.png", output_image)
    log_image(f"rangeLogs/testranged{count}.png", ranged_image)
    log_image(f"edgeLogs/testedges{count}.png", dilated_edges)

    return pdf_bounding_boxes

def parse_boxes(boxes, path, program,year):
    """
        Extracts the text from inside each bounding box
    """
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
                      "unit_value":"1", #placeholder
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
                      "unit_value":"1", #placeholder
                      "program": program,
                      "year":year}
        class_list.append(class_to_add)
    return class_list