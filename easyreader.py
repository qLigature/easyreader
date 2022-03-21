from tabula import read_pdf

def parse_page(pdf_filepath, page):

    # coordinates will dictate where tabula will scan the table
    # refer to https://github.com/tabulapdf/tabula-java/wiki/Using-the-command-line-tabula-extractor-tool#grab-coordinates-of-the-table-you-want
    page1_area = (364.066, 14.503, 693.547, 579.753)
    page2_area = (55.409, 13.759, 678.672, 580.497)
    # to get column coordinates, select the column manually in tabula app and get coordinates
    columns = "--columns 83,160,190,258,288,364,400,435,480,533"

    if page == 1:
        coordinates = page1_area
    else:
        coordinates = page2_area

    raw_df = read_pdf(pdf_filepath, pages=[page], area=coordinates, pandas_options={'header':None}, options=columns)
    return raw_df

test_filepath = "./test_data/220320_220305.pdf"
page = 3
parse_page(test_filepath, page)[0].to_csv('./output.csv')