This project was written for the "Python For Everybody" specialisation course from the University of Michigan. 

The project takes data from https://opendata.ecdc.europa.eu/covid19/casedistribution/json/

databasebuilder.py: this code reads the json file from the link, retrieves the data and puts it in a database "covid.sqlite"

cases.py: this code takes the cases information and produces a visualisation of the 15 countries that have the most cases.

Creates: casestotal.js, which is used by casestotal.htm to do the visualisation


deaths.py: same, for number of total deaths per country.

Creates: deathstotal.js, which is used by deathstotal.htm to do the visualisation