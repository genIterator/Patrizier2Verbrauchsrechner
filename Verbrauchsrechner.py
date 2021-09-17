from io import SEEK_CUR
import os

class Verbrauchsrechner(object):

    def __init__(self, efficencyTableName = "ProductionEfficency.csv", priceListName = "ProductList.csv", consumptionListName = "ConsumptionValues.csv", stadtName = ""):
        self.efficencyTableName = efficencyTableName
        self.priceListName = priceListName
        self.consumptionListName = consumptionListName
        # Index aller Städte
        self.staedteListe = {}
        # Warenverbrauch der Einwohner (Reich, Wohlhabend, Arm)
        self.verbrauchsListe = []
        # einfache Liste aller Waren
        self.warenNamen = []
        # berechneter Verbrauch basierend auf Einwohnern und Reisedauer
        self.stadtVerbrauch = []
        self.stadtName = stadtName
        self.lastWaren = ["Eisenerz", "Fisch", "Fleisch", "Getreide", "Hanf", "Holz", "Wolle", "Ziegel"]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.efficencyTableName!r}, {self.priceListName!r}, {self.consumptionListName!r}, {self.staedteListe!r}, {self.warenNamen}, {self.stadtVerbrauch})"
    def __str__(self):
        return f"{self.__class__.__name__} Attribute:\n {self.efficencyTableName}\n {self.priceListName}\n {self.consumptionListName}\n {self.staedteListe}\n\n {self.verbrauchsListe}\n\n {self.warenNamen}\n\n {self.stadtVerbrauch}\n\n"

    def prepareTables(self):
        # create city list
        with open(self.efficencyTableName) as fHandle:
            line = fHandle.readline()
            line = line.strip()
            for nr, name in enumerate(line.split(";")):
                self.staedteListe[name] = nr        
        # create verbrauchsliste
        with open(self.consumptionListName) as fHandle:
            for nr, line in enumerate(fHandle):
                line = line.strip()
                if nr == 0:
                    if line == "Ware;Reiche;Wohlhabende;Arme":
                        continue
                    else:
                        raise Exception(f"Format of Consumption file not as expected!")
                currEff = line.split(";")
                self.verbrauchsListe.append([])
                for value in currEff[1:]:
                    self.verbrauchsListe[nr-1].append(float(value))
                self.warenNamen.append(currEff[0])
    
    def calculateConsumption(self, reiche: int, wohlis: int , arme: int, tage: int = 7):
        # Wochenverbrauch je 1k je Klasse
        for index, warenListe in enumerate(self.verbrauchsListe):
            currVerbrauch = warenListe[0] * (reiche / 1000) * (tage / 7)
            self.stadtVerbrauch.append(currVerbrauch)
            currVerbrauch = warenListe[1] * (wohlis / 1000) * (tage / 7)
            self.stadtVerbrauch[index] += currVerbrauch
            currVerbrauch = warenListe[2] * (arme / 1000) * (tage / 7)
            self.stadtVerbrauch[index] += currVerbrauch
            self.stadtVerbrauch[index] = round(self.stadtVerbrauch[index])

    def printVerbrauch(self, warenVerbrauch, descriptionText = "\n Gesamtverbrauch der Stadt: \n", stadt = ""):
        gesamtFass = 0      
        efficiency = self.parseEfficencyTable(stadt) 
        printEff = False
        
        if len(efficiency) > 1:
            printEff = True
        else:
            printEff = False
        
        print(descriptionText)
        if printEff:
            print("|    Ware    | Verbrauch | Effizienz |")
            print("--------------------------------------")
        else:
            print("|    Ware    | Verbrauch |")
            print("--------------------------")
        
        for index, ware in enumerate(self.warenNamen):
            if printEff:
                print(f"| {ware:10} | {str(warenVerbrauch[index]):9} | {efficiency[index]:9} |")
            else:
                print(f"| {ware:10} | {str(warenVerbrauch[index]):9} |")
            if ware in self.lastWaren:
                gesamtFass += int(warenVerbrauch[index]) * 10
            else:
                gesamtFass += int(warenVerbrauch[index])
        if printEff:
            print("--------------------------------------")
        else:
            print("--------------------------")
        print(f"| Gesamt: {gesamtFass:10} Fass|")

    def printStadtverbrauch(self):
        self.printVerbrauch(self.stadtVerbrauch)

    def printHanseVerbrauch(self, gesamtWarenVerbrauch):
        self.printVerbrauch(gesamtWarenVerbrauch, "\n Gesamtverbrauch der Städte: \n")

    def getStadtLineForUpdate(self):
        line = self.stadtName + ";"
        for value in self.stadtVerbrauch:
            line += str(value) + ";"
        line = line[:-1]
        #line += "\n"
        return line.encode("Utf-8")

    def updateGesamtverbrauchDatei(self, fileName:str):
        data = []
        alreadyAppended = False

        with open(fileName,mode="rb") as fHandle:
            data = fHandle.readlines()        

        if data:
            for idx, line in enumerate(data):
                values = line.decode("Utf-8").strip().split(";")
                #values = line.split(";")
                if (values[0] == self.stadtName):
                    # found city in file, update the line
                    if (len(data) == idx +1):
                        #last line has no new line
                        data[idx] += "\n".encode("Utf-8")
                    data[idx] = self.getStadtLineForUpdate()
                    if (len(data) != idx+1):
                        # lines in the middle need line break
                        data[idx] += "\n".encode("Utf-8")
                    alreadyAppended = True
                    break
        if not alreadyAppended:
            # line will be added at the end
            data[len(data)-1] += "\n".encode("Utf-8")
            data.append(self.getStadtLineForUpdate())   

        with open(fileName, mode="+wb") as fHandle:
            fHandle.writelines(data)

    def calculateHanseVerbrauch(self, fileName:str):
        gesamtWarenVerbrauch = [0 for val in range(len(self.warenNamen))]
        with open(fileName) as fHandle:
            for line in fHandle:
                line = line.strip()
                values = line.split(";")
                for idx, value in enumerate(values[1:]):
                    gesamtWarenVerbrauch[idx] += int(value)
        return gesamtWarenVerbrauch

    def printAllCities(self, fileName):
        with open(fileName) as fHandle:
            for line in fHandle:
                line = line.strip()
                values = line.split(";")
                if (len(values) > 1):
                    # workaround for city names
                    self.printVerbrauch(values[1:], f"\n Gesamtverbrauch der Stadt: {values[0]} \n", values[0])

    def calculateTravelTime(self, fileName: str):
        schiff = ""
        start = ""
        ziel = self.stadtName
        traveltime = 7
        columnIndex = 0
        data = []

        with open(fileName, "rb") as fHandle:
            for line in fHandle:
                data.append(line.decode("Utf-8").strip().split(","))
        
        if len(data) >= 7:
            # format of first 4 lines is fixed
            schiff = data[0][1]
            start = data[1][1] 
            targetCities = data[2]
            startcities = data[3]

            if len(targetCities) > 2 and targetCities[0] == "Ziel":
                #find route
                for index, city in enumerate(targetCities[1:]):
                    if (city == ziel) and (startcities[index] == start):
                        # increase index by 1 because first column is skipped!
                        columnIndex = index +1
                        break

                if data[4][columnIndex] == schiff:
                    # assume 75% usage of ship for whole route
                    # table lists 100% and 50%
                    traveltime = int(data[5][columnIndex]) + int(data[6][columnIndex])
                else:
                    #iterate over other lines to find ship
                    if len(data) >= 10:
                        for rowindex, entry in enumerate(data [7:]):
                            if (entry[0] == "Schiff") and (entry[columnIndex] == schiff):
                                # iteration starts not at line 0!
                                offset = 7
                                # assume 75% usage of ship for whole route
                                # table lists 100% and 50%
                                traveltime = int(data[rowindex+offset+1][columnIndex]) + int(data[rowindex+offset+2][columnIndex])
                    else:
                        print("Angegebener Schiffstyp konnte nicht gefunden werden. Reisezeit konnte nicht berechnet werden!")
        else:
            print(f"Format of {fileName} is wrong!")   
        print(f"Berechnete Reisezeit: {traveltime} Tage")     
        return traveltime

    def parseEfficencyTable(self, stadt = ""):
        data = []
        efficiency = []
        # workaround if cities are read from file
        if self.stadtName != "" and stadt == "":
            stadt = self.stadtName
        if self.stadtName != "":
            with open(self.efficencyTableName, "rb") as fHandle:
                for line in fHandle:
                    data.append(line.decode("Utf-8").strip().split(","))        
            for line in data:
                if (line[0] == stadt):
                    efficiency = line[1:]
        return efficiency
