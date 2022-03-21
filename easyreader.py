import pandas as pd
from tabula import read_pdf

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1

from easydownload import download_soa

def get_pdf_path():
    while True:
        path = input("Enter the PDF's filepath: ")
        try:
            pdf = open(path, 'rb')
            del pdf
            return path
        except:
            print("Error: Invalid path entered. Try again.")


def parse_pdf(pdf_filepath, include_pagenum=False):

    # Gets total number of pages in PDF
    # Credits to: https://stackoverflow.com/questions/45841012/how-can-i-get-the-total-count-of-total-pages-of-a-pdf-file-using-pdfminer-in-pyt
    pdf = open(pdf_filepath, 'rb')
    parser = PDFParser(pdf)
    document = PDFDocument(parser)
    total_pages = resolve1(document.catalog['Pages'])['Count']
    del pdf

    raw_df = []

    # Iterate through all PDF pages, parse them, then combine them all into a single dataframe
    for page in range(1, total_pages + 1):
        raw_df.append(parse_page(pdf_filepath, page, include_pagenum))
        print("Page {} done".format(page))

    df = pd.concat(raw_df)

    return df


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


def add_page_col(df, page):
    page_num = [page for i in range(0, len(df))]
    df['PageNum'] = page_num
    return df


def process_df(df):
    col_names = ["PostedDate", "TrxDate", "Transaction", "Description", "BU",
                 "OBUIDClass", "VATAmount", "Debit", "Credit", "TotalAmount", "RunningBalance", "Page"]

    # Delete excess rows outside of ones aligned with a non-empty RunningBalance cell
    df = df.set_axis(col_names, axis=1).dropna(
        subset=["RunningBalance"]).reset_index(drop=True)

    # Trim OBUIDClass column to contain only plate numbers whenever possible
    df = format_plate(df)
    return df


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


def generate_output(pdf_filepath, df):
    # Get filename of PDF and save it as the filename of the CSV output
    pdf_filename = pdf_filepath.split("/")[-1].split(".pdf")[0]
    output_filepath = "./csv/" + pdf_filename + ".csv"

    try:
        df.to_csv(output_filepath)
    except PermissionError:
        print("Error: Cannot create output file. Close any related files or programs then try again.")
        input()
        df.to_csv(output_filepath)

    print("PDF successfully parsed. Output data is in {}.".format(output_filepath))

pdf_filepath = download_soa()

# pdf_filepath = get_pdf_path()

df = parse_pdf(pdf_filepath, True)
df = process_df(df)

generate_output(pdf_filepath, df)
