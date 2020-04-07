# THIS CODE READS THE DATABASE COVID.SQLITE, CALCULATES THE TOTAL OF DEATHS AND VISUALISE THE TOTAL PER COUNTRY

import sqlite3
import time
import zlib


# OPEN DATABASE
conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()


# RETRIEVE COUNTRY, DATE & CASES AND PUT THEM IN A DICTIONARY
cur.execute('SELECT name, acdate, deaths FROM Country JOIN Date JOIN Info ON country_id = Country.id AND date_id = Date.id')
deaths = dict()
countries = list()
for deaths_info in cur :
    deaths[(deaths_info[0], deaths_info[1])] = deaths_info[2]
    if deaths_info[0] not in countries: countries.append(deaths_info[0])
#print(countries)


# CALCULATE TOTAL OF CASES FOR EACH COUNTRY TO SELECT THE 15 MOST AFFECTED
totaldeaths = dict()
for c in countries:
    counter_deaths = 0
    for i in deaths:
        if i[0] == c:
            counter_deaths = counter_deaths + deaths.get(i,0)
    totaldeaths[c] = counter_deaths
#print(totaldeaths)

sorteddeaths = sorted(totaldeaths.items(), key=lambda x: x[1], reverse = True)
sorteddeaths = sorteddeaths[:15]
print(sorteddeaths)


# MODIFY A JAVASCRIPT FILE THAT REPRESENTS THE NUMBER OF CASES PER COUNTRY
fhand = open('deathstotal.js','w')
fhand.write("deathstotal = [ ['Total Deaths Per Country','Total Deaths', { role: 'style' }]")
for c in sorteddeaths:
    fhand.write(",\n['"+c[0]+"',"+str(c[1])+",'red']")
fhand.write("\n];\n")
fhand.close()

print("Output written to deathstotal.js")
print("Open deathstotal.htm to visualize the data")
