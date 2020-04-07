# THIS CODE RETRIEVES THE JSON FILE FROM https://opendata.ecdc.europa.eu/covid19/casedistribution/json/, PARSES THE JSON FILE AND CREATES A DATABASE WITH THE DATA RETRIEVED

import urllib.request, urllib.parse, urllib.error
import json
import ssl
import sqlite3

# IGNORE SSL CERTIFICATE ERRORS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# CREATE DATABASE
conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Country;
DROP TABLE IF EXISTS Date;
DROP TABLE IF EXISTS Info;

CREATE TABLE Country (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE,
    population INTEGER
);

CREATE TABLE Date (
    id    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    acdate  TEXT UNIQUE,
    year INTEGER,
    month INTEGER,
    day INTEGER
);

CREATE TABLE Info (
    country_id   INTEGER,
    date_id     INTEGER,
    cases        INTEGER,
    deaths       INTEGER,
    PRIMARY KEY (country_id, date_id)
)
''')


# RETRIEVE JSON FILE AND LOAD IT
url = input('Enter URL: ')
if len(url) < 1:
    url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
print('Retrieving...',url)

connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()
json_data = json.loads(data)


# RETRIEVE INFO IN JSON DATA AND FILL UP DATABASE
for entry in json_data["records"]:

    date = entry["dateRep"]
    year = entry["year"]
    month = entry["month"]
    day = entry["day"]
    cases = entry["cases"]
    deaths = entry["deaths"]
    country = entry["countriesAndTerritories"]
    population = entry["popData2018"]
    #print(date, cases, deaths, country, population)

    cur.execute('INSERT OR IGNORE INTO Date (acdate,year,month,day) VALUES ( ?, ?, ?, ? )', ( date, year, month, day ) )
    cur.execute('SELECT id FROM Date WHERE acdate = ? ', (date, ))
    date_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Country (name,population) VALUES ( ?, ? )', ( country, population ) )
    cur.execute('SELECT id FROM Country WHERE name = ? ', (country, ))
    country_id = cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Info (country_id, date_id, cases, deaths) VALUES ( ?, ?, ?, ? )', (country_id, date_id, cases, deaths ) )

    conn.commit()
