class Verbrauchsrechner(object):

    def __init__(self, efficencyTableName = "ProductionEfficency.csv", priceListName = "ProductList.csv", consumptionListName = "ConsumptionValues.csv"):
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
        self.gesamtVerbrauch = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.efficencyTableName!r}, {self.priceListName!r}, {self.consumptionListName!r}, {self.staedteListe!r}, {self.warenNamen}, {self.gesamtVerbrauch})"
    def __str__(self):
        return f"{self.__class__.__name__} Attribute:\n {self.efficencyTableName}\n {self.priceListName}\n {self.consumptionListName}\n {self.staedteListe}\n\n {self.verbrauchsListe}\n\n {self.warenNamen}\n\n {self.gesamtVerbrauch}\n\n"


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
            self.gesamtVerbrauch.append(currVerbrauch)
            currVerbrauch = warenListe[1] * (wohlis / 1000) * (tage / 7)
            self.gesamtVerbrauch[index] += currVerbrauch
            currVerbrauch = warenListe[2] * (arme / 1000) * (tage / 7)
            self.gesamtVerbrauch[index] += currVerbrauch
            self.gesamtVerbrauch[index] = round(self.gesamtVerbrauch[index])

    def printGesamtverbrauch(self):
        print("\n Gesamtverbrauch der Stadt: \n")
        print("|    Ware    | Verbrauch |")
        print("--------------------------")
        for index, ware in enumerate(self.warenNamen):
            print(f"| {ware:10} | {str(self.gesamtVerbrauch[index]):9} |")
