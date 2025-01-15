import fitz
from collections import defaultdict
from PIL import Image
import cv2
#import easyocr
import numpy as np
import os
from difflib import SequenceMatcher

#for testing
PDF_PATH = os.getcwd() + r"\maps\22-23\Business Intelligence Analytics - Advising Map - '22-'23.pdf"
MAP_DIR= os.getcwd() + r"\maps\22-23"

# reader = easyocr.Reader(['en'],gpu=False)


#use fitz to open the pdf
def get_nparray_from_pdf(path):
    doc = fitz.open(path)

    page = doc[0]
    pix = page.get_pixmap(dpi=500)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    return cv_image

def text_extract(path,box):
    doc = fitz.open(path)

    page = doc[0]

    # text=page.get_textbox(box)
    text = page.search_for("term")
    # print(page.get_drawings())
    print(text)

def pdf_coord_to_png(x0_pdf,x1_pdf,y0_pdf,y1_pdf,image,page):
    width_png, height_png = image.shape[1], image.shape[0]
    width_pdf, height_pdf = page.rect.width, page.rect.height  # Example PDF size (A4 in points, 8.5"x11" at 72 DPI)

    #calculate scaling factors
    scale_x = width_png / width_pdf
    scale_y = height_png / height_pdf

    x0_png = round(x0_pdf * scale_x)
    y0_png = round((y0_pdf * scale_y))
    x1_png = round(x1_pdf * scale_x)
    y1_png = round((y1_pdf * scale_y))

    return x0_png,x1_png,y0_png,y1_png

def log_image(name, image):
    cv2.imwrite(os.getcwd()+ "\\imgLogs\\" +name,image)

def check_if_inside(recA,recB):
    #print(f"comparing {recA} and {recB}")
    #recA
    xA0 = recA['x']
    yA0 = recA['y']
    xA1 = recA['x']+recA['w']
    yA1 = recA['y']+recA['h']

    #recB
    xB0 = recB['x']
    yB0 = recB['y']
    xB1 = recB['x'] + recB['w']
    yB1 = recB['y'] + recB['h']

    #check if each point in A is inside B
    if xA0>xB0 and yA0>yB0 and xA1<xB1 and yA1<yB1:
        return True
    return False

def parse_map(path, count):
    image = get_nparray_from_pdf(path)
    output_image = image.copy()

    doc = fitz.open(path)
    page = doc[0]

    # blurred_image = cv2.bilateralFilter(image,9,75,75)
    #log_image(f"testblurred{count}.png",blurred_image)

    #define the colour range to look in
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([200, 200, 200])
    ranged_image = cv2.inRange(image, lower_black, upper_black)


    log_image(f"testranged{count}.png",ranged_image)

    # edge detection
    edges = cv2.Canny(ranged_image, 60,80)
    kernel = np.ones((5, 5), np.uint8)

    #then dilate them to make them larger
    dilated_edges = cv2.dilate(edges, kernel, iterations=6)

    #we then want to find the two top-leftmost occurrences of the word term!
    term_recs = page.search_for("term")
    sorted(term_recs, key=lambda x: x[0])
    sorted(term_recs, key=lambda y: y[0])
    term_recs=[term_recs[0],term_recs[1]]
    term_centers=[]
    for i in range (0,len(term_recs)):
        x0=round(term_recs[i].x0)
        x1 = round(term_recs[i].x1)
        y0 = round(term_recs[i].y0)
        y1 = round(term_recs[i].y1)

        x0,x1,y0,y1=pdf_coord_to_png(x0,x1,y0,y1,image,page)
        w=x1-x0
        h=y1-y0

        #this just draws a little lump where the bounding rec would be
        #crop = image[y:y + h, x:x + w]
        #cv2.rectangle(image, (x0, y0), (x0 + w, y0 + h), (255, 255, 0), 88)
        #log_image(f"boundLogs/term.png", image)

        #what we really care about here is the x value of the center
        center_x=round((x0+x1)/2)
        term_centers.append({'term':i+1,'x':center_x,'y':y0})


        cv2.line(output_image, (center_x, y0), (center_x, image.shape[0]), (0, 255, 0), 4)

    #display the intersect lines
    log_image(f"intersectLogs/term{count}.png", output_image)
    print(term_centers)


    #display the dilated edges
    log_image(f"testedges{count}.png", dilated_edges)  # Debugging: Show edges


    #find contours
    contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    boxes=[]
    for contour in contours:
        #bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)


        #get rid of bound boxes above the term blocks
        if y<term_centers[0]['y']:
            continue

        #get rid of bound boxes not intersecting a term block
        #term I
        if x < term_centers[0]['x'] < x+w:
            term=1
        #term II
        elif x < term_centers[1]['x'] < x+w:
            term=2
        else:
            continue

        boxes.append({'x':x,'y':y,"w":w,"h":h,"term":term})
        #cv2.rectangle(output_image, (x, y), (x + w, y + h),colour, 7)

    #now we want to eliminate "nested" boxes
    #this can be done with contour heirarchies but i was having difficulty
    print(len(boxes))
    to_remove=[]
    for boxA in boxes:
        for boxB in boxes:
            if check_if_inside(boxA,boxB):
                to_remove.append(boxA)
                #print(f"{boxA} inside {boxB}")
                break
    for box in to_remove:
        boxes.remove(box)

    print(len(boxes))
    bound_count = 0
    for box in boxes:
        if box['term'] == 1:
            colour=(224,13,224)
        else:
            colour=(13,34,224)
        #must be a nicer way to unpack these
        x=box['x']
        y=box['y']
        w=box['w']
        h=box['h']

        crop = image[y:y + h, x:x + w]
        cv2.rectangle(output_image, (x, y), (x + w, y + h), colour, 7)
        log_image(f"boundLogs/bound{bound_count}.png", crop)
        bound_count = bound_count + 1


    #     rec=fitz.Rect(x0, y0, x1, y1)
    #     #image.crop(x0,y0,x1,y)
    #     # print(rec)
    #     # text=text_extract(path,rec)
    #     # print(text)
    #
    # print(boxes[1])
    # print(boxes[2])
    # print(check_if_inside(boxes[1],boxes[2]))
    log_image(f"testbounded{count}.png",output_image)


#gives similarity of two strings, to account for typos in the pdf names
def string_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def parse_maps_directory(dir):
    programs=defaultdict(dict)

    #check errors check errors check erros >:(
    for pdf in os.listdir(dir):
        if os.path.splitext(pdf)[1] != '.pdf':
            continue

        #check that it's actually a pdf blah bloah blah

        #split the title
        pdf_arr=pdf.split('-')

        #get the title, spell check it... some of the pdfs were not spelled the same >:(
        programTitle=pdf_arr[0].strip()
        for program in programs.keys():
            similarity=string_similarity(programTitle,program)
            if similarity > 0.9:
               # print(f"{program} and {programTitle} have {similarity}")
                programTitle=program

        #check for year/if it is a 2-year program
        if "year1" in pdf.lower().replace(" ",""):
            programs[programTitle]['year1']=dir+"\\"+pdf
        elif "year2" in pdf.lower().replace(" ",""):
            programs[programTitle]['year2'] = dir+"\\"+pdf
        else:
            programs[programTitle]['year0']=dir+"\\"+pdf


    return(programs)

def parse_programs(programs):
    count=0
    for program in programs.keys():
        for term in programs[program].keys():
            print(programs[program][term])
            parse_map(programs[program][term],count)
            return
            count+=1


text_extract(PDF_PATH,"s")

programs=parse_maps_directory(MAP_DIR)
parse_programs(programs)

#
# #
# parse_map(path)