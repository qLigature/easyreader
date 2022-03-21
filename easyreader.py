from tabula import read_pdf

def parse_page(pdf_filepath, page):

    # coordinates will dictate where tabula will scan the table
    # see: https://stackoverflow.com/questions/56065307/how-can-i-stop-tabula-from-automatically-dropping-empty-columns/71553990#71553990
    page1_area = (364.066, 15, 693.547, 580)
    page2_area = (55.409, 15, 678.672, 580)
    # to get column coordinates, select the column manually in tabula app and get coordinates
    columns = "--columns 83,160,190,258,288,364,400,435,480,533"

    if page == 1:
        coordinates = page1_area
    else:
        coordinates = page2_area

    raw_df = read_pdf(pdf_filepath, pages=[page], area=coordinates, options=columns, pandas_options={'header':None})
    return raw_df[0]

test_filepath = "./test_data/220304_220217.pdf"
page = 3
# parse_page(test_filepath, page).to_csv('./output.csv')

# test columns for all pages
# total_pages = 38
# for page in range(1, total_pages):
#     print(len(parse_page(test_filepath, page).columns))