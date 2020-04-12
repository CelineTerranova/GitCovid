# THIS CODE READS THE DATABASE COVID.SQLITE, CALCULATES THE TOTAL OF DEATHS AND VISUALISE THE TOTAL PER COUNTRY

import sqlite3
import time
import zlib


# OPEN DATABASE
conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()


# RETRIEVE COUNTRY, DATE & CASES AND PUT THEM IN A DICTIONARY
cur.execute('SELECT name, population, acdate, deaths FROM Country JOIN Date JOIN Info ON country_id = Country.id AND date_id = Date.id')
deaths = dict()
countries = list()
for deaths_info in cur :
    deaths[(deaths_info[0], deaths_info[2])] = deaths_info[3]
    if deaths_info[0] not in countries: countries.append((deaths_info[0],deaths_info[1]))
#print(countries)


# CALCULATE TOTAL OF CASES FOR EACH COUNTRY TO SELECT THE 15 MOST AFFECTED
totaldeaths = dict()
for c in countries:
    counter_deaths = 0
    for i in deaths:
        if i[0] == c[0]:
            counter_deaths = counter_deaths + deaths.get(i,0)
    totaldeaths[c] = counter_deaths
#print(totaldeaths)

sorteddeaths = sorted(totaldeaths.items(), key=lambda x: x[1], reverse = True)
sorteddeaths = sorteddeaths[:15]
print('Absolute deaths:')
print(sorteddeaths)

# USE THE POPULATION OF THESE 15 COUNTRIES TO CALCULATE THE RELATIVE NUMBER OF CASES
reldeaths = list()
for c in sorteddeaths:
    cname = c[0]
    fraction = 0.0
    for p in countries:
        if p[0] == cname[0]:
            fraction = c[1] / p[1]
            reldeaths.append((cname[0],fraction))
            break
#print(relcases)

sortedreldeaths = sorted(reldeaths, key=lambda x: x[1], reverse = True)
print('Relative deaths:')
print(sortedreldeaths)


# MODIFY A JAVASCRIPT FILE THAT REPRESENTS THE NUMBER OF CASES PER COUNTRY
fhand = open('deathstotal.js','w')
fhand.write("deathstotal = [ ['Total Deaths Per Country','Total Deaths', { role: 'style' }]")
for c in sorteddeaths:
    fhand.write(",\n['"+c[0][0]+"',"+str(c[1])+",'red']")
fhand.write("\n];\n")
fhand.close()

# MODIFY A JAVASCRIPT FILE THAT REPRESENTS THE RELATIVE NUMBER OF CASES PER COUNTRY
fhand = open('deathsrelative.js','w')
fhand.write("deathsrelative = [ ['Relative Deaths Per Country','Relative Deaths', { role: 'style' }]")
for c in sortedreldeaths:
    fhand.write(",\n['"+c[0]+"',"+str(c[1])+",'red']")
fhand.write("\n];\n")
fhand.close()

print("Output written to deathstotal.js and deathsrelative.js")
print("Open deathstotal.htm and deathsrelative.htm to visualize the data")
