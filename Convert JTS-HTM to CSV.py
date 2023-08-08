#nombre a archivo csv
#11 to fix bug jupiter bft
# Using list List Comprehensions

from bs4 import BeautifulSoup
import datetime
import time
import numpy as np
from numpy import asarray
import csv
import shutil, os
from pathlib import Path
import glob

logFilesPath = ""
globalHeaders = []
globalLL = []
globalUL = []
dataScrap = ['\n', '•', '\xa0', '\r', '\t', ',']
headersWritten = False
totalFilesProcessed = 0
file_name_flag = False
csvFileName = ''

def generateCSVFileName():
    current_time = time.localtime()
    return time.strftime('%m-%d-%Y_%H-%M-%S', current_time)
     
def attachToCSV(file_Data):
    global headersWritten
    global file_name_flag
    global csvFileName
    #GET THE ID: with the TIAL Path file name
    #GET THE CSV NAME: with the tester name and the actual timestamp
    if not file_name_flag:
        csvFileName = generateCSVFileName()
        file_name_flag = True
    #csvFileName = file_Data[4]
    with open('CSV_' + csvFileName +'.csv','ab') as f:
        if not headersWritten:
            headersWritten = True
            np.savetxt(f, (globalHeaders, file_Data), delimiter="," , fmt="%s")
        else:
            np.savetxt(f, asarray([file_Data]), delimiter="," , fmt="%s")

def fileScrapper(data):
    for scrap in dataScrap:
        data = data.replace(scrap, '')
    return data

def htmTimeFormarterForCSV(dateTime):
    date_time_obj = datetime.datetime.strptime(str(dateTime),"%A %B %d %Y %I:%M:%S %p")
    return str(date_time_obj.date())+ " "+ str(date_time_obj.time())    

def filesProcessing():
    
    global globalHeaders
    global globalLL
    global globalUL
    global headersWritten
    global totalFilesProcessed
    
    for filePathName in glob.glob(logFilesPath):
        file_Data_Table = [[],[],[],[],[],[],[],[],[],[],[],]
        #TestGroup,TestName,TestStatus,Parametrics,IsMeasurement,LowerLimit,UpperLimit,Measurement,MeasurementUnit,ElapsedTime,ExecutionTime
        file_Headers = ['ID']
        file_Data = []
        file_LL = []
        file_UL = []
        file_Data.append(os.path.split(filePathName)[1][:-4])
        
        with open (filePathName) as currentFile:
            bsFile = BeautifulSoup(currentFile, "html.parser")
            
            allH3Tags = bsFile.find_all('h3')
            for tagH3 in allH3Tags:
                if ':' in tagH3.text:
                    file_Headers.append(fileScrapper(tagH3.text[ : tagH3.text.find(':')]))
                    if file_Headers[len(file_Headers)-1] in 'Test Result':
                        file_Data.append(fileScrapper(tagH3.text[tagH3.text.find(':') + 2 : tagH3.text.find('\n')]))
                    else:
                        file_Data.append(fileScrapper(tagH3.text[tagH3.text.find(':') + 2 : ]))
                        
            file_Data[2] = htmTimeFormarterForCSV(file_Data[2])
            file_Data[3] = htmTimeFormarterForCSV(file_Data[3])
            
            allTDTags = bsFile.find_all('td')
            secondTR = bsFile.find_all('center', limit=13)
            del secondTR[:2]
            del allTDTags[:12]
            i = 0
            while len(allTDTags) > 0:
                file_Data_Table[i].append(fileScrapper(allTDTags.pop(0).text))
                i+=1
                if i==len(secondTR):
                    i=0
            
            file_Data.extend(file_Data_Table[7])
            file_Headers.extend(file_Data_Table[1])
            
            #Getting the perfect headers that will be the global ones, only 1 header for all csv file.
            if len(file_Headers) > len(globalHeaders):
                headersWritten = False
                globalHeaders = file_Headers.copy()
                globalLL = file_Data_Table[5].copy()
                globalUL = file_Data_Table[6].copy()
            
            attachToCSV(file_Data)
            
            print(file_Data[0])
            totalFilesProcessed += 1
            
def main():
    global logFilesPath
    path = os.getcwd()
    logFilesPath = path + "\\html\\*.htm"    
    filesProcessing()
    print('Total Files Proccesed:', totalFilesProcessed)
        
main()