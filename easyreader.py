import pandas as pd
from tabula import read_pdf


def parse_page(pdf_filepath, page, include_pagenum=False):

    # Coordinates will dictate where Tabula will scan the table
    # To get column coordinates, select the column manually in Tabula app and check script output
    # see: https://stackoverflow.com/questions/56065307/how-can-i-stop-tabula-from-automatically-dropping-empty-columns/71553990#71553990
    page1_area = (364, 15, 694, 580)
    page2_area = (55, 15, 679, 580)
    columns = "--columns 83,160,190,258,288,364,400,435,480,533"
    coordinates = page1_area if page == 1 else page2_area

    raw_df = read_pdf(pdf_filepath, pages=[
                      page], area=coordinates, options=columns, pandas_options={'header': None})

    if include_pagenum:
        return add_page_col(raw_df[0], page)

    return raw_df[0]


def format_plate(df):

    for row_idx in df.index:
        # Reload transactions don't have plate numbers and so can be skipped
        transaction_type = df.loc[row_idx, "Transaction"]
        if transaction_type == "Reload":
            continue

        # IDClass column is formatted with "/" seperator
        id_class = df.loc[row_idx, "OBUIDClass"]
        plate_no = id_class.split("/")[1]
        if plate_no == "":
            continue

        # Save plate number to IDClass column
        df.loc[row_idx, "OBUIDClass"] = plate_no
    return df


def add_page_col(df, page):
    page_num = [page for i in range(0, len(df))]
    df['PageNum'] = page_num
    return df


test_filepath = "./test_data/220320_220305.pdf"
total_pages = 47

raw_df = []
col_names = ["PostedDate", "TrxDate", "Transaction", "Description", "BU",
             "OBUIDClass", "VATAmount", "Debit", "Credit", "TotalAmount", "RunningBalance", "Page"]

for page in range(1, total_pages + 1):
    raw_df.append(parse_page(test_filepath, page, True))
    print("Page {} done.".format(page))

df = pd.concat(raw_df)
df = df.set_axis(col_names, axis=1).dropna(
    subset=["RunningBalance"]).reset_index(drop=True)

df = format_plate(df)

df.to_csv('./output.csv')
