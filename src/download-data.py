import urllib.request

def downloadFile(url, filename):
  urllib.request.urlretrieve(url, filename)

# downloadFile("http://www.digitallook.com/cgi-bin/dlmedia/price_download.cgi/download.csv?action=download&csi=190159&start_day=1&start_month=1&start_year=2019&end_day=2&end_month=1&end_year=2019&type=csv", "/coding/financial-data/csv-files/test.csv")