import pandas as pd

def load_student_data(path,CLASS_DATAFRAME):
    STUDENT_DATAFRAME=pd.read_excel(path, engine='openpyxl')
    #combine the subject+catalog into one cell
    STUDENT_DATAFRAME['code'] = STUDENT_DATAFRAME['Subject'] + ' ' + STUDENT_DATAFRAME['Catalog']

    #first we want to map the weird abbreviations to something more readable
    #we do this by checking each abbrev and seeing what classes overlap
    #i.e ITDBADMIN -> IT Database Administration
    abbreviations=STUDENT_DATAFRAME['Acad Plan'].unique()
    program_names = CLASS_DATAFRAME['program'].unique()

    for abbrev in abbreviations:
        #get all the classes a student in a certain abbreviation took
        prog_df=STUDENT_DATAFRAME[STUDENT_DATAFRAME['Acad Plan'] == abbrev]
        abbrevs_classes=prog_df['code']

        #get the program that shares the most overlap with the courses
        overlap=CLASS_DATAFRAME[CLASS_DATAFRAME['code'].isin(abbrevs_classes)]
        best_guess=overlap['program'].value_counts().idxmax()
        max_overlap=overlap['program'].value_counts().tolist()[0]

        # print(f"{abbrev} means {best_guess} with {overlap['program'].value_counts()[0]} overlap")

        #if the overlap is very little don't say anything with certainty!
        if max_overlap > 5:
            STUDENT_DATAFRAME['Acad Plan'] = STUDENT_DATAFRAME['Acad Plan'].replace(abbrev, best_guess)
        else:
            STUDENT_DATAFRAME['Acad Plan'] = STUDENT_DATAFRAME['Acad Plan'].replace(abbrev, best_guess)

    #then combine the subject+catalog into one cell
    STUDENT_DATAFRAME['code'] = STUDENT_DATAFRAME['Subject'] + ' ' + STUDENT_DATAFRAME['Catalog']
    return STUDENT_DATAFRAME