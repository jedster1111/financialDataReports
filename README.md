A small python script to scrape some financial data, store some historical data for each share and then generate a report of the closing values of all tracked shares.

The code is pretty messy and very hardcoded for a specific spreadsheet. So definitely not built for generic usage or for maintainability.  
Uses `.csv` files for input and output.

# Usage

Tested with Python 3.7.2  
Must provide a `main.csv` file in the `csv-files/` directory.  
Run `python src/main.py` to generate data.
