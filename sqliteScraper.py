import ldap
import sqlite3
from sqliteQueries import *


#Create and configure LDAP connection
DOMAIN = "ldaps://directory.srv.ualberta.ca"
ROOT_DN="ou=calendar,dc=ualberta,dc=ca"
ldap.set_option(ldap.OPT_SIZELIMIT,20000)
# print(ldap.get_option(ldap.OPT_SIZELIMIT))
page_control = ldap.controls.libldap.SimplePagedResultsControl(True, size=20000, cookie='')


#Create and initialize sqlite db
dbCon,dbCurs = connect("./calendar.db")
drop_tables(dbCon,dbCurs)
define_tables(dbCon,dbCurs)

def main():
    #If this line fails then the service is likely gone or moved
    ldapCon = ldap.initialize(DOMAIN)

    '''
    https://ldap.com/basic-ldap-concepts/
    https://hub.packtpub.com/configuring-and-securing-python-ldap-applications-part-2/
    https://sites.google.com/a/ualberta.ca/open-data/calendar-data
    http://www.novell.com/coolsolutions/tip/18274.html
    https://medium.com/@alpolishchuk/pagination-of-ldap-search-results-with-python-ldap-845de60b90d2

    A working example of using ldaps, where dn (distinguished name) is the "directory" that we are entering.
    You can only get attributes that pertains to the current dn, like how you can only access
    files from a particular folder rather than from the parent folder.

    dn="term=1326,ou=calendar,dc=ualberta,dc=ca"
    print(ldapCon.compare_s(dn,"term", b"1326"))
    '''

    #initialize list
    termDnList = []

    #Find all terms add them to the db
    termList = ldapCon.search_s(ROOT_DN,ldap.SCOPE_ONELEVEL)
    for termDn,termAttr in termList:

        #Use the attribute dictionary for each term into insertTerm
        insertTerm(termAttr,dbCon,dbCurs)
        termDnList.append(termDn)
    

    
    #Find all children of the terms (courses) and add them to the db
    for termDn in termDnList:

        #There can be over 1000 entries for courses, so must use pagination to get results.
        #For some reason it is possible to abuse pagination by having a page size > 1000 and
        #not have the script throw a max results error, so this is not typical pagination.
        courseList = ldapCon.search_ext_s(termDn,
                               ldap.SCOPE_ONELEVEL,
                               "(objectClass=uOfACourse)", 
                               [],
                               serverctrls=[page_control])

        for courseDn,courseAttr in courseList:
            insertCourse(courseAttr,dbCon,dbCurs)
    
        #Find all classes of each term and add them to the db
        classList = ldapCon.search_ext_s(termDn,
                               ldap.SCOPE_SUBTREE,
                               "(objectClass=uOfAClass)", 
                               [],
                               serverctrls=[page_control])

        for classDn,classAttr in classList:
            insertClass(classAttr,dbCon,dbCurs)

        #Find all classTimes in the term and add them to the db
        classTimeList = ldapCon.search_ext_s(termDn,
                               ldap.SCOPE_SUBTREE,
                               "(objectClass=uOfAClassTime)", 
                               [],
                               serverctrls=[page_control])

        for classTimeDn,classTimeAttr in classTimeList:
            insertClassTime(classTimeAttr,dbCon,dbCurs)

        #Find all textbooks in the term and add them to the db
        textbookList = ldapCon.search_ext_s(termDn,
                               ldap.SCOPE_SUBTREE,
                               "(objectClass=uOfATextbook)", 
                               [],
                               serverctrls=[page_control])

        for textbookDn,textbookAttr in textbookList:
            insertTextbook(textbookAttr,dbCon,dbCurs)


    print("Data collected successfully")




if __name__== "__main__":
    main()
