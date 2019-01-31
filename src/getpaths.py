import os

def getCsvDirectoryPath():
  return os.path.dirname(os.path.realpath(__file__)) + "/../csv-files"

def getTempFilePath():
  return getCsvDirectoryPath() + "/temp"

def getHistoryFilePath():
  return getCsvDirectoryPath() + "/history"

def getReportsFilePath():
  return getCsvDirectoryPath() + "/reports"
