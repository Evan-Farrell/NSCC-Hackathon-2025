import os

from PyPDF2 import PdfReader,PdfWriter
from PyPDF2.generic import create_string_object
path=os.getcwd()+ r"\template.pdf"


def update_field(obj,val):
    obj.update({
        "/V": create_string_object(val)
    })
def unpack_data(data):
    mapped_data=[]
    for i,term in enumerate(data.keys(),start=1):
        for j,course in enumerate(data[term],start=1):
            code_tag="code"+str(i) + str(j)
            class_tag="class" +str(i) + str(j)
            val_tag="val"+str(i) + str(j)

            code_val=data[term][course]['combobox_value']
            label_val = data[term][course]['label1_value']
            label2_val = data[term][course]['label2_value']

            mapped_data.append((code_tag, code_val))
            mapped_data.append((class_tag, label_val))
            mapped_data.append((val_tag, label2_val))
    print(mapped_data)
def gen_pdf(mappings):

    reader = PdfReader(path)
    page = reader.pages[0]
    annotations = page.get("/Annots")
    annot_dicts={}

    for annot in annotations:
        annot_obj = annot.get_object()


        if "/FT" in annot_obj and annot_obj["/FT"] == "/Tx":
            #updated text field
            update_field(annot_obj,"")
            annot_dicts[annot_obj.get("/T")]=annot_obj

    return
    for field in annot_dicts:
        print(field)
    return

    writer=PdfWriter()
    writer.add_page(page)

    output_pdf = "export.pdf"
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Modified PDF saved as '{output_pdf}'")


sample={'term_widget_group_1': {'combobox_1': {'combobox_value': 'W1002', 'label1_value': 'widgets 201', 'label2_value': 1.5}, 'combobox_2': {'combobox_value': 'W1000', 'label1_value': 'widgets 101', 'label2_value': 1}, 'combobox_3': {'combobox_value': None, 'label1_value': None, 'label2_value': None}, 'combobox_4': {'combobox_value': 'W1000', 'label1_value': 'widgets 101', 'label2_value': 1}, 'combobox_5': {'combobox_value': None, 'label1_value': None, 'label2_value': None}, 'combobox_6': {'combobox_value': 'W1002', 'label1_value': 'widgets 201', 'label2_value': 1.5}}, 'term_widget_group_2': {'combobox_1': {'combobox_value': None, 'label1_value': None, 'label2_value': None}, 'combobox_2': {'combobox_value': None, 'label1_value': None, 'label2_value': None}, 'combobox_3': {'combobox_value': 'W1000', 'label1_value': 'widgets 101', 'label2_value': 1}, 'combobox_4': {'combobox_value': 'W1000', 'label1_value': 'widgets 101', 'label2_value': 1}, 'combobox_5': {'combobox_value': 'W1000', 'label1_value': 'widgets 101', 'label2_value': 1}, 'combobox_6': {'combobox_value': 'W1000', 'label1_value': 'widgets 101', 'label2_value': 1}}}
unpack_data(sample)


gen_pdf(sample)
