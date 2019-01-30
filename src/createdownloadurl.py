def createDownloadUrl(id, startDate, endDate):
  return f"http://www.digitallook.com/cgi-bin/dlmedia/price_download.cgi/download.csv?action=download&csi={id}&start_day={startDate.day}&start_month={startDate.month}&start_year={startDate.year}&end_day={endDate.day}&end_month={endDate.month}&end_year={endDate.year}&type=csv"
