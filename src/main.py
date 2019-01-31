from createdownloadurl import createDownloadUrl
from downloaddata import downloadFile
from getpaths import getCsvDirectoryPath, getTempFilePath, getHistoryFilePath, getReportsFilePath

import datetime
import os, os.path
import csv
import shutil

def main():
  daysInPast = int(input("How many days' of data do you want to download?"), 10)

  today = datetime.datetime.now()
  yesterday = today - datetime.timedelta(daysInPast)

  print(today.date())

  csvFilePath = getCsvDirectoryPath()
  tempPath = getTempFilePath()
  historyPath = getHistoryFilePath()
  reportsPath = getReportsFilePath()

  reportFieldNames = ["id", "name", "symbol", "historicalLow", "historicalHigh", "closingPrice", "indicator"]

  with open(csvFilePath + "/main.csv", mode="r") as csv_file, open(reportsPath + f"/{today.date()}.csv", mode="w", newline="") as reportFile: # Parse main file and create today's report
    reader = csv.DictReader(csv_file, delimiter="\t")
    reportWriter = csv.DictWriter(reportFile, reportFieldNames)
    
    reportWriter.writeheader()

    for row in reader:
      id, symbol, name, historicalLow, historicalHigh  = row["Web Financial Group download code"], row["Symbol"], row["Name"], row["Share Price Low"], row["Share Price High"]
      if id:
        print(f"Downloading data for {name} ({symbol}) with id: {id}")
        downloadFile(createDownloadUrl(id, yesterday, today), tempPath + "/temp.csv")

        if not os.path.isfile(historyPath + f"/{name}.csv"): # Check if history file exists, create one if not
          open(historyPath + f"/{name}.csv", "w+")

        with open(tempPath + "/temp.csv", mode="r") as downloadedFile, open(historyPath + f"/{name}.csv", mode="r") as historyFile, open(historyPath + f"/{name}_temp.csv", mode="w", newline="") as tempFile:
            historyReader = csv.DictReader(historyFile)
            fieldnames = ["date", "closingPrice"]

            downloadedReader = csv.DictReader(downloadedFile)
            tempWriter = csv.DictWriter(tempFile, fieldnames)

            allDownloadedLines = list(downloadedReader)

            closingPrice = allDownloadedLines[-1]["Close Price"]

            indicator = str(int((float(closingPrice) - float(historicalLow)) * 100 / (float(historicalHigh) - float(historicalLow)))) + "%"

            # Create report
            reportWriter.writerow({"id": id, "name": name, "symbol": symbol, "historicalLow": historicalLow, "historicalHigh": historicalHigh, "closingPrice": closingPrice, "indicator": indicator })

            downloadedFile.seek(0)
            next(downloadedReader)    

            tempWriter.writeheader()

            rowsToWrite = []
            seen = set() # Creating set of already downloaded dates
            for historyRow in historyReader:
              seen.add(historyRow["date"])
              rowsToWrite.append(historyRow)

            for downloadedRow in downloadedReader:
              if downloadedRow["Date"] not in seen:
                print(f"Added row for {downloadedRow['Date']}")
                rowsToWrite.append({"date": downloadedRow["Date"], "closingPrice": downloadedRow["Close Price"]})

            rowsToWrite.sort(key=lambda currentRow: datetime.datetime.strptime(currentRow["date"], "%d-%b-%Y"))
            tempWriter.writerows(rowsToWrite)

        shutil.move(historyPath + f"/{name}_temp.csv", historyPath + f"/{name}.csv")              

      else:
        print(f"{name} ({symbol}) doesn't have an id stored!")

main()
