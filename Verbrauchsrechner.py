#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import sys
import os
import os.path


defaultCityList = ["Aalborg", "Bergen", "Bremen", "Brügge", "Danzig", "Edinburg", "Groningen", 
                   "Hamburg", "Köln", "Ladoga", "London", "Lübeck", "Malmö", "Novgorod",
                   "Oslo", "Reval", "Riga", "Ripen", "Rostock", "Scarborough", "Stettin",
                   "Stockholm", "Thorn", "Visby"]

defaultWaren = ["Bier", "Eisenerz", "Eisenwaren", "Felle", "Fisch", 
                "Fleisch", "Getreide", "Hanf", "Holz", "Honig", 
                "Keramik", "Leder", "Pech", "Salz", "Tran", "Tuch", 
                "Wein", "Wolle", "Ziegel"]


def main():
    parser = argparse.ArgumentParser(description='Programm Patrizier 2, um die Verbrauchswerte der Einwohner einer Stadt zu berechnen.')
    parser.add_argument("-c", "--city", help="Stadt die versorgt werden soll.", type=str, required=True)
    parser.add_argument("-r", "--reiche", help="Anzahl der Reichen in der Stadt.", type=int, required=True)
    parser.add_argument("-w", "--wohlis", help="Anzahl der Wohlhabenden in der Stadt", type=int, required=True)
    parser.add_argument("-a", "--arme", help="Anzahl der Armen in der Stadt", type=int, required=True)
    parser.add_argument("-t", "--time", help="gesamte Reisezeit für die Stadt (hin & zurück)", type=int, required=True)
    args = parser.parse_args()
    
    
    print(args)


if __name__ == "__main__":
    main()