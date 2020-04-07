# THIS CODE TAKES THE DATABASE CREATED BY DATABASEBUILDER AND SORTS THE DATES BY ASCENDING ORDER, THEN CALCULATES ACCUMULATIVE DEATHS AND CASES, THEN PUTS THAT INFO INTO A NEW DATABASE "CLEANCOVID"

# Assuming you created your original table like so:
#
# CREATE TABLE my_table (rowid INTEGER PRIMARY KEY, name TEXT, somedata TEXT) ;
# You can create another sorted table like so:
#
# CREATE TABLE my_ordered_table (rowid INTEGER PRIMARY KEY, name TEXT, somedata TEXT) ;
# INSERT INTO my_ordered_table (name, somedata) SELECT name,somedata FROM my_table
# ORDER BY name ;
