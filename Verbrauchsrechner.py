class Product(object):
    def __init__(self, nr, name, buy, sell, typ):
        self.nr = nr
        self.name = name
        self.buy = buy
        self.sell = sell
        self.type = typ



class Verbrauchsrechner(object):

    def __init__(self, efficencyTableName = "ProductionEfficency.csv", priceListName = "ProductList.csv", consumptionListName = "ConsumptionValues.csv"):
        self.efficencyTableName = efficencyTableName
        self.priceListName = priceListName
        self.consumptionListName = consumptionListName
        # Index aller Städte
        self.staedteListe = {}
        # Index aller Waren
        self.warenListe = {}
        # Warenverbrauch der Einwohner (Reich, Wohlhabend, Arm)
        self.verbrauchsListe = []
        # Produktionseffizienz aller Waren
        self.produktionsListe = []
        # Detailinfos zu allen Waren
        self.warenInfo = []

        self.warenNamen = []
        self.gesamtVerbrauch = []

    def __repr__(self):
        return f"{self.__class__.__name__}({self.efficencyTableName!r}, {self.priceListName!r}, {self.consumptionListName!r}, {self.staedteListe!r}, {self.warenListe!r}, {self.produktionsListe!r})"
    def __str__(self):
        return f"{self.__class__.__name__} Attribute:\n {self.efficencyTableName}\n {self.priceListName}\n {self.consumptionListName}\n {self.staedteListe}\n\n {self.warenListe}\n\n {self.verbrauchsListe}\n\n {self.produktionsListe}"


    def prepareTables(self):

        # create city list
        with open(self.efficencyTableName) as fHandle:
            line = fHandle.readline()
            line = line.strip()
            for nr, name in enumerate(line.split(";")):
                self.staedteListe[name] = nr
            #print(self.staedteListe)
        
        # create product, warenlist and wareninfo 
        with open(self.priceListName) as fHandle:
            for nr, line in enumerate(fHandle):
                if nr == 0:
                    line = line.strip()
                    if line.startswith("Product;Buy;Sell;Weight"):
                        continue
                    else:
                        raise Exception(f"Format of {self.priceListName} file does not fit expected format: Product;Buy;Sell;Weight!")
                line = line.strip()
                values = line.split(";")
                #print(values[0])
                # nr -1 since first line is csv format!
                self.warenListe[values[0]] = nr-1
                #print(values)
                #print(nr-1)
                self.warenInfo.append(Product(nr-1, values[0], values[1], values[2], values[3]))
                #print(self.warenInfo[nr-1].name)
        
        # create verbrauchsliste
        with open(self.consumptionListName) as fHandle:
            for nr, line in enumerate(fHandle):
                line = line.strip()
                if nr == 0:
                    # print(line)
                    if line == "Ware;Reiche;Wohlhabende;Arme":
                        continue
                    else:
                        raise Exception(f"Format of Consumption file not as expected!")
                currEff = line.split(";")
                # print(currEff)
                # skip warenname
                self.verbrauchsListe.append([])
                for value in currEff[1:]:
                    self.verbrauchsListe[nr-1].append(float(value))
                self.warenNamen.append(currEff[0])
    # print(self.verbrauchsListe)
    
    def calculateConsumption(self, reiche: int, wohlis: int , arme: int, tage: int = 7):
        #print("calculating...")
        #gesamtVerbrauch = []
        # Wochenverbrauch je 1k je Klasse
        for index, warenListe in enumerate(self.verbrauchsListe):
            currVerbrauch = warenListe[0] * (reiche / 1000) * (tage / 7)
            self.gesamtVerbrauch.append(currVerbrauch)
            currVerbrauch = warenListe[1] * (wohlis / 1000) * (tage / 7)
            self.gesamtVerbrauch[index] += currVerbrauch
            currVerbrauch = warenListe[2] * (arme / 1000) * (tage / 7)
            self.gesamtVerbrauch[index] += currVerbrauch
            self.gesamtVerbrauch[index] = round(self.gesamtVerbrauch[index])
        #print("done.")
        #return gesamtVerbrauch

    def printGesamtverbrauch(self):
        print("\n Gesamtverbrauch der Stadt: \n")
        print("|    Ware    | Verbrauch |")
        print("--------------------------")
        for index, ware in enumerate(self.warenNamen):
            print(f"| {ware:10} | {str(self.gesamtVerbrauch[index]):9} |")
