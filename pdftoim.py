import fitz
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import cv2
import numpy as np

pdf_path = r"C:\Users\kanem\PycharmProjects\hackathon\NSCC-Hackathon-2025\maps\22-23\Business Intelligence Analytics - Advising Map - '22-'23.pdf"

#use fitz to open the pdf
def get_nparray_from_pdf(path):
    doc = fitz.open(pdf_path)

    page = doc[0]
    pix = page.get_pixmap(dpi=500)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    return cv_image


image = get_nparray_from_pdf(pdf_path)

#define the range to look in
lower_black = np.array([0, 0, 0])
upper_black = np.array([200, 200, 200])

# Create a mask for black parts of the image
ranged_image = cv2.inRange(image, lower_black, upper_black)


cv2.imwrite("test.png",ranged_image)

#blur it to pronounce the edges
blurred_image = cv2.GaussianBlur(ranged_image,(3,3),0)

#edge detection
#first find them then dilate them to make them larger
edges = cv2.Canny(blurred_image, 60,80)
kernel = np.ones((5, 5), np.uint8)
dilated_edges = cv2.dilate(edges, kernel, iterations=10)
cv2.imwrite("testedges.png", dilated_edges)  # Debugging: Show edges

#find contours
contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

output_image = image.copy()
for contour in contours:

    #approx the contour to a polygon
    epsilon = 0.005 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    #check if the approxed shape has 4 sides
    if len(approx) == 4:  # Ignore small areas
        #bounding box
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(output_image, (x, y), (x + w, y + h), (255, 255, 0), 7)

cv2.imwrite("detectedtest.png", output_image)
