
import argparse
import os
from Verbrauchsrechner import Verbrauchsrechner

def main():
    parser = argparse.ArgumentParser(description='Programm Patrizier 2, um die Verbrauchswerte der Einwohner einer Stadt zu berechnen.')
    parser.add_argument("-c", "--city", help="Stadt die versorgt werden soll.", type=str, required=False)
    parser.add_argument("-r", "--reiche", help="Anzahl der Reichen in der Stadt.", type=int, required=False)
    parser.add_argument("-w", "--wohlis", help="Anzahl der Wohlhabenden in der Stadt", type=int, required=False)
    parser.add_argument("-a", "--arme", help="Anzahl der Armen in der Stadt", type=int, required=False)
    parser.add_argument("-t", "--time", help="gesamte Reisezeit für die Stadt (hin & zurück)", type=int, required=False)
    parser.add_argument("-g", "--gesamt", action="store_true", help="Berechnung des Gesamtverbrauchs für gespeicherte Städte", required=False)
    parser.add_argument("-u", "--update", action="store_true", help="Speichern der aktuellen Stadt in der Gesamtverbrauchsliste", required=False)
    parser.add_argument("-p", "--printall", action="store_true", help="Ausgabe des Verbrauchs aller gespeicherten Städte", required=False)
    args = parser.parse_args()
    
    rechner = Verbrauchsrechner(stadtName=args.city)
    rechner.prepareTables()

    if (args.reiche and args.wohlis and args.arme and args.time):
        rechner.calculateConsumption(args.reiche, args.wohlis, args.arme, args.time)
        rechner.printStadtverbrauch()
        if (args.update == True):
            if (args.city == ""):
                print("Fehler: Update der Gesamtliste erfordert einen Städtenamen!")
            else:
                fileName = os.getcwd()+"/Hanseverbrauch.txt"
                rechner.updateGesamtverbrauchDatei(fileName)
    else:
        if (args.printall == False) and (args.gesamt == False):
            print("Kein Stadtverbrauch berechnet, ggf. fehlen Argumente.")

    if (args.printall):
        fileName = os.getcwd()+"/Hanseverbrauch.txt"
        rechner.printAllCities(fileName)

    if (args.gesamt):
        fileName = os.getcwd()+"/Hanseverbrauch.txt"
        rechner.printHanseVerbrauch(rechner.calculateHanseVerbrauch(fileName))

if __name__ == "__main__":
    main()