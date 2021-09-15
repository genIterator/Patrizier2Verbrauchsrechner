# Patrizier2Verbrauchsrechner
Tool for Patrizier 2 Gold (Patrician 3) to calculate consumption of goods

* Use the following options to calculate the consumption for one city:
    * -r \<number of rich inhabitants>
    * -w \<number of wealthy inhabitants>
    * -a \<number of poor inhabitants>
    * -t \<traveltime in days to the city> (may be omitted, see below)
* In order to store the calculated values, the following parameters are required as well:
    * -c \<name of the city>
    * -u
* If traveltime is omitted, it is calculated from the "Traveltime.csv"
    * modify the "Traveltime.csv" depending on the used ship and the kontor
    * currently, only travel times starting in Stettin are provided
    * currently, only travel times with ship type Kraier are provided
* Print the consumption for all stored cities:
    * -g
* Print the consumption of each stored city:
    * -p
    
Examples:
1. Calculating consumption for one city:
```
python main.py -r 100 -w 400 -a 600 -t 7
```
2. Storing calculated consumption values:
```
python main.py -r 100 -w 400 -a 600 -t 7 -c Danzig -u
```
3. Calculating consumption for one city and calulating consumption for whole Hanse (not including the provided city!):
```
python main.py -r 100 -w 400 -a 600 -t 7 -c Danzig -g
```
4. Output consumption of all stored cities and calculating consumption for whole Hanse:
```
python main.py -p -g
```