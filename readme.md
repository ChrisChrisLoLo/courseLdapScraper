# CourseLdapScraper
This is a scraper that collects information from the UofA calandar LDAP system.
This information includes course information, class times, when classes are offered, credits offered, and much more.

This code requires that python-ldap be installed, which can be done with this link.
Several prerequisite programs are needed before python-ldap can be installed.

## Status
Currently, the script available copies the LDAP system "verbatim", as in most of the schema matches that of the current LDAP system. There are pros and cons of this approach. The schema currently has multiple redundencies and probably fails 3NF, likley making it unsuitable for any write operations. However, this schema has a TON of information which can be further extracted from. Explanations of each column can be found here https://sites.google.com/a/ualberta.ca/open-data/calendar-data.

## Future Plans
More scripts can be made to further process/refactor the data. This data is supposedly updated frequently (daily-ish), and more course data becomes available when more courses appear on bear tracks (around march). What ever information beartracks has, the LDAP system, and by extension, the SQLite db has. Check the date of the SQLite file to see if it is up to date.

## How To Use
There are two things that can be done
1) Take the SQL file directly.
    If the file is fairly recent simply take the db file, read the documentation above, and do with the data as you will.
2) Run the script.
    If the db file is fairly dated, running the script may be necessary. 
    The script requires both python-ldap as well as sqlite3, and any prerequisites those programs might need. https://www.python-             ldap.org/en/latest/installing.html. 
    Running the script will generate a new DB file with updated data, which should match information beartracks has, atleast for the next couple of years.
