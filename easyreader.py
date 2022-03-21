import pandas as pd
from tabula import read_pdf
import warnings

def parse_page(pdf_filepath, page):

    # coordinates will dictate where tabula will scan the table
    # see: https://stackoverflow.com/questions/56065307/how-can-i-stop-tabula-from-automatically-dropping-empty-columns/71553990#71553990
    page1_area = (364, 15, 694, 580)
    page2_area = (55, 15, 679, 580)
    # to get column coordinates, select the column manually in tabula app and get coordinates
    columns = "--columns 83,160,190,258,288,364,400,435,480,533"

    if page == 1:
        coordinates = page1_area
    else:
        coordinates = page2_area

    raw_df = read_pdf(pdf_filepath, pages=[page], area=coordinates, options=columns, pandas_options={'header':None})
    return raw_df[0]

test_filepath = "./test_data/220320_220305.pdf"
total_pages = 47

raw_df = []
col_names = ["PostedDate", "TrxDate", "Transaction", "Description", "BU", "OBUIDClass", "VATAmount", "Debit", "Credit", "TotalAmount", "RunningBalance"]

for page in range(1, total_pages+1):
    raw_df.append(parse_page(test_filepath, page))
    print("Page {} done.".format(page))

raw_df = pd.concat(raw_df)
raw_df.set_axis(col_names, inplace=True, axis=1)
raw_df.dropna(subset=["RunningBalance"], inplace=True)
raw_df.reset_index(inplace=True, drop=True)

raw_df.to_csv('./output.csv')