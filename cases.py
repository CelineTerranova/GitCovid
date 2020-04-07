# THIS CODE READS THE DATABASE COVID.SQLITE, CALCULATES THE TOTAL OF CASES AND VISUALISE THE TOTAL PER COUNTRY

import sqlite3
import time
import zlib


# OPEN DATABASE
conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()


# RETRIEVE COUNTRY, DATE & CASES AND PUT THEM IN A DICTIONARY
cur.execute('SELECT name, acdate, cases FROM Country JOIN Date JOIN Info ON country_id = Country.id AND date_id = Date.id')
cases = dict()
countries = list()
for cases_info in cur :
    cases[(cases_info[0], cases_info[1])] = cases_info[2]
    if cases_info[0] not in countries: countries.append(cases_info[0])
#print(countries)


# CALCULATE TOTAL OF CASES FOR EACH COUNTRY TO SELECT THE 15 MOST AFFECTED
totalcases = dict()
for c in countries:
    counter_cases = 0
    for i in cases:
        if i[0] == c:
            counter_cases = counter_cases + cases.get(i,0)
    totalcases[c] = counter_cases
#print(totalcases)

sortedcases = sorted(totalcases.items(), key=lambda x: x[1], reverse = True)
sortedcases = sortedcases[:15]
print(sortedcases)


# MODIFY A JAVASCRIPT FILE THAT REPRESENTS THE NUMBER OF CASES PER COUNTRY
fhand = open('casestotal.js','w')
fhand.write("casestotal = [ ['Total Cases Per Country','Total Cases', { role: 'style' }]")
for c in sortedcases:
    fhand.write(",\n['"+c[0]+"',"+str(c[1])+",'blue']")
fhand.write("\n];\n")
fhand.close()

print("Output written to casestotal.js")
print("Open casestotal.htm to visualize the data")
