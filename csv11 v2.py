#nombre a archivo csv
#11 to fix bug jupiter bft

from bs4 import BeautifulSoup
import datetime
import numpy as np
import csv
import shutil, os
from pathlib import Path
import glob



def generarCsv():
    head, tail = os.path.split(name)
    print(tail)
    tail=tail[:-4]
    listaFinal = infoList + listaPruebas
    listaFinal.insert(0,['ID',tail])
    print(listaFinal)
    csvName = listaFinal[4][1]
    print(csvName)
    tester = csvName[:-3]
    #fixing bug for Jupiter
    if tester == ' JUPITER_BFT':
        listaFinal[78][1]=r'getprop ro.boot.secure_cpu\n1\njupiter ~>'
        listaFinal[109][1] =r'getprop ro.boot.secure_cpu\n1\nganymede ~>'

    column = []
    column2 = []
    for ii in range(len(listaFinal)):
        xxx = listaFinal[ii][0]
        column.append(xxx)

    for j in range(len(listaFinal)):
        yyy = listaFinal[j][1]
        yyy = yyy.replace("\n","")
        yyy = yyy.replace(",",";")
        yyy = yyy.replace("\r","")
        yyy = yyy.replace("#","")
        column2.append(yyy)

    column3 = [column , column2]
    with open(csvName+'.csv','ab') as f:
        #newresult = np.random.rand(2, 3)
        np.savetxt(f, column3, delimiter="," , fmt="%s")
        
path = os.getcwd()
print(path)
#Your folder with HTM files path here:
fullPath = path + "\\html\\*.htm" 
for name in glob.glob(fullPath):
#for name in glob.glob("C:\\TE\\TestLogs\\html\\*.htm"):   # Loop for search all the .htm files
    print(name)
    with open ( name ) as fp:                             # open the html
        soup = BeautifulSoup(fp, "html.parser")

        a = soup.find_all('h3')                            #find all the .htm H3
        li = []
        for i in range(len(a)):                             #Loop for all the h3
            headers = a[i].text

            li.append(headers)

        li[7] = li[7][0:17]
        li = li[1:]
        infoList = []
        for k in range(len(li)):
            spl= li[k].split(":", 1)
            infoList.append(spl)
            #print(infoList)
        b = soup.find_all('td')
        liTd = []
        for q in range(len(b)):
            table = b[q].text
            liTd.append(table)

        liTd = liTd[12:]

        dataName =[]
        dataStatus =[]
        dataValue =[]
        for t in range(1,len(liTd),11):
            dataName.append(liTd[t])

        for y in range(2,len(liTd),11):
            dataStatus.append(liTd[y])

        for u in range(7,len(liTd),11):
            dataValue.append(liTd[u])
        listaVergas = []

        for lista in range(len(dataName)):
            x = dataName[lista], dataValue[lista], dataStatus[lista]
            x = list(x)
            listaVergas.append(x)
        #print(listaVergas)
        listaPruebas = listaVergas.copy()
        for www in range(len(listaPruebas)):
            listaPruebas[www] = listaPruebas[www][:2]
        #print(listaPruebas)

        m = infoList[1][1] =infoList[1][1].replace(",","")
        n = infoList[2][1] = infoList[2][1].replace(",","")
        infoList[1][1] = m[1:]
        infoList[2][1] = n[1:]
        #print(infoList[1][1])
        date_time_obj = datetime.datetime.strptime(str(infoList[1][1]),"%A %B %d %Y %I:%M:%S %p")
        infoList[1][1] = str(date_time_obj.date())+ " "+ str(date_time_obj.time())
        date_time_obj = datetime.datetime.strptime(infoList[2][1],"%A %B %d %Y %I:%M:%S %p")
        infoList[2][1] = str(date_time_obj.date())+ " "+ str(date_time_obj.time())
        #print(infoList[2][1])

        if (infoList[6][1]) == " FAIL":
            print("Lo logramos")
            z = 0
            for danonino in range(len(listaVergas)):
                padre = listaVergas[danonino]
                for hijo in range(3):
                    #print(padre[hijo])
                    if(padre[hijo] == "FAIL"):
                        if z == 0:
                            laFalla = padre[0]
                            z =z+1
                        else:
                            break
            infoList[6][1] = laFalla
            generarCsv()

        else:
            infoList[6][1] = "PASS"
            generarCsv()
