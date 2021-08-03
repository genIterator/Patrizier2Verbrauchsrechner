
import argparse
import sys
import os
import os.path
from Verbrauchsrechner import Verbrauchsrechner



def main():
    parser = argparse.ArgumentParser(description='Programm Patrizier 2, um die Verbrauchswerte der Einwohner einer Stadt zu berechnen.')
    parser.add_argument("-c", "--city", help="Stadt die versorgt werden soll.", type=str, required=False)
    parser.add_argument("-r", "--reiche", help="Anzahl der Reichen in der Stadt.", type=int, required=True)
    parser.add_argument("-w", "--wohlis", help="Anzahl der Wohlhabenden in der Stadt", type=int, required=True)
    parser.add_argument("-a", "--arme", help="Anzahl der Armen in der Stadt", type=int, required=True)
    parser.add_argument("-t", "--time", help="gesamte Reisezeit für die Stadt (hin & zurück)", type=int, required=True)
    args = parser.parse_args()
    
    rechner = Verbrauchsrechner()
    rechner.prepareTables()
    rechner.calculateConsumption(args.reiche, args.wohlis, args.arme, args.time)
    rechner.printGesamtverbrauch()


if __name__ == "__main__":
    main()