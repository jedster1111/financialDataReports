from createdownloadurl import createDownloadUrl
from downloaddata import downloadFile
from getpaths import getCsvDirectoryPath, getTempFilePath, getHistoryFilePath

import datetime
import os, os.path
import csv
import shutil

def main():
  daysInPast = int(input("How many days' of data do you want to download?"), 10)

  today = datetime.datetime.now()
  yesterday = today - datetime.timedelta(daysInPast)

  csvFilePath = getCsvDirectoryPath()
  tempPath = getTempFilePath()
  historyPath = getHistoryFilePath()

  with open(csvFilePath + "/main.csv", mode="r") as csv_file: # Parse main file
    reader = csv.DictReader(csv_file, delimiter="\t")

    for row in reader:
      id, symbol, name  = row["Web Financial Group download code"], row["Symbol"], row["Name"]
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

            tempWriter.writeheader()

            rowsToWrite = []

            seen = set()
            for historyRow in historyReader: # Creating set of already downloaded dates
              seen.add(historyRow["date"])
              tempWriter.writerow(historyRow)


            for downloadedRow in downloadedReader:
              if downloadedRow["Date"] not in seen:
                parsedDate = datetime.datetime.strptime(downloadedRow["Date"], "%d-%b-%Y")    
                print(f"Added row for {downloadedRow['Date']}")
                tempWriter.writerow({"date": downloadedRow["Date"], "closingPrice": downloadedRow["Close Price"]})

        shutil.move(historyPath + f"/{name}_temp.csv", historyPath + f"/{name}.csv")              

      else:
        print(f"{name} ({symbol}) doesn't have an id stored!")

main()
