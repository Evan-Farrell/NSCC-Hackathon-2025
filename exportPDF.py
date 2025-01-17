from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import create_string_object
import os

FORMAT_PATH=os.getcwd()+r"/resources/format.pdf"


def gen_pdf(data,header):

    def unpack_data(data):
        mapped_data = []

        for i, term in enumerate(data.keys(), start=1):
            for j, course in enumerate(data[term], start=1):
                code_tag = "code" + str(i) + str(j)
                class_tag = "class" + str(i) + str(j)
                val_tag = "val" + str(i) + str(j)

                code_val = data[term][course]['combobox_value']
                label_val = data[term][course]['label1_value']
                label2_val = data[term][course]['label2_value']

                mapped_data.append((code_tag, code_val))
                mapped_data.append((class_tag, label_val))
                mapped_data.append((val_tag, label2_val))
        return mapped_data

    def update_field(obj, val):
        obj.update({
            "/V": create_string_object(val)
        })

    mappings=unpack_data(data)
    mappings.append(("name",header['name']))
    mappings.append(("prog",header['program']))
    mappings.append(("id",header['id']))
    reader = PdfReader(FORMAT_PATH)
    page = reader.pages[0]
    annotations = page.get("/Annots")
    annot_dicts={}

    for annot in annotations:
        annot_obj = annot.get_object()

        if "/FT" in annot_obj and annot_obj["/FT"] == "/Tx":
            #updated text field
            update_field(annot_obj,"")
            annot_dicts[annot_obj.get("/T")]=annot_obj



    for field,val in mappings:
        if val is None:
            val=""
        update_field(annot_dicts[field],str(val))


    writer=PdfWriter()
    writer.add_page(page)

    output_pdf = os.getcwd()+r"\latexFunctions\export.pdf"
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"Modified PDF saved as '{output_pdf}'")
    return 1