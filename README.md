# Easy Reader

A Python script to parse Statement of Account PDFs generated by Easytrip's Customer Account Management System (CAMS) and output a .csv file containing parsed data for further processing and analysis.

## Usage

Run easyreader.py and pass in the path of the PDF file to be parsed. The program will then generate a .csv file in the same folder.

## Requirements

Use `pip install` for the following if needed:

- pandas
- tabula-py
- pdfminer
- pyyaml
- selenium
- chromedriver-autoinstaller

## TODO

| Functionality | Status |
| - | - |
| Generate dataframe from PDF file via tabula-py | Done |
| Ensure resulting dataframe has equal columns (even with empty or broken data) | Done |
| Add option to include page column for denoting where the transaction is located in the PDF file | Done |
| Format OBUIDClass column into plate numbers whenever possible | Done |
| Save dataframe as .csv file | Done |
| Add filtering certain types of transactions | Planned |
| Add statistics for certain transactions, including overcharging | Planned |
| Add automatic downloading of SOA via Selenium | Ongoing |
| Add online dashboard functionality for automatic real-time viewing of balance and transactions | Planned |

## Links

- `Easytrip Customer Management System` [Website](https://myeasytripcams.easytrip.ph/CAMS/)
- `tabula-py` [Wiki](https://tabula-py.readthedocs.io/en/latest/)
- `How to define empty columns for tables with tabula-py` [Stack Overflow](https://stackoverflow.com/questions/56065307/how-can-i-stop-tabula-from-automatically-dropping-empty-columns/71553990#71553990)
