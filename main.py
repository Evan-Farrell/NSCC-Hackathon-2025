import pandas as pd


SAMPLE_PATH=r"C:\Users\kanem\PycharmProjects\hackathon\NSCC-Hackathon-2025\SampleData\Template Data.xlsx"

#pip install openpyxl for xlsx reader
df=pd.DataFrame(pd.read_excel(SAMPLE_PATH, engine='openpyxl'))
print(df)