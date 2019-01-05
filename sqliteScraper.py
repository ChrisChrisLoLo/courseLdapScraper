import ldap
import sqlite3
from sqliteQueries import *

DOMAIN = "ldaps://directory.srv.ualberta.ca"
ROOT_DN="ou=calendar,dc=ualberta,dc=ca"


#Create and initialize sqlite db
dbCon,dbCurs = connect("./calendar.db")
drop_tables(dbCon,dbCurs)
define_tables(dbCon,dbCurs)


def main():
    #If this line fails then the service is likely gone or moved
    ldapCon = ldap.initialize(DOMAIN)
    #ldapCon.get_attributes()
    
    print(ldapCon.compare_s(ROOT_DN,"ou", b"1370"))
    dn="term=1326,ou=calendar,dc=ualberta,dc=ca"
    print(ldapCon.compare_s(dn,"term", b"1326"))

    '''
    https://ldap.com/basic-ldap-concepts/
    https://hub.packtpub.com/configuring-and-securing-python-ldap-applications-part-2/
    https://sites.google.com/a/ualberta.ca/open-data/calendar-data

    A working example of using ldaps, where dn (distinguished name) is the "directory" that we are entering.
    You can only get attributes that pertains to the current dn, like how you can only access
    files from a particular folder rather than from the parent folder.

    dn="term=1326,ou=calendar,dc=ualberta,dc=ca"
    print(ldapCon.compare_s(dn,"term", b"1326"))
    '''

    #initialize lists
    termDnList = []
    courseDnList = []
    classDnList = []
    classTimeDnList = []
    textbookDnList = []

    #Find all terms add them to the db
    termList = ldapCon.search_s(ROOT_DN,ldap.SCOPE_ONELEVEL)
    for term in termList:
        
        termDn = term[0]
        termAttr = term[1]

        #Use the attribute dictionary for each term into insertTerm
        insertTerm(termAttr,dbCon,dbCurs)
        termDnList.append(termDn)
    
    #Find all children of the terms and add them to the db
    for termDn in termDnList:
        courseList = ldapCon.search(termDN,ldap.SCOPE_ONELEVEL)

        for course in courseList:

            courseDn = course[0]
            courseAttr = course[1]

            insertCourse(courseAttr,dbCon,dbCurs)
            courseDnList.append(courseDn)

    
    print()
    print("hihi")

if __name__== "__main__":
    main()