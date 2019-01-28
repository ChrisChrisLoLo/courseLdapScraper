import sqlite3
from dbTransformQueries import *

OLD_DB = "../calendar.db"
NEW_DB = "./transformed.db"

#Create and initialize the sqlite db
oldCon,oldCurs = connect(OLD_DB)
newCon,newCurs = connect(NEW_DB)


drop_new_tables(newCon,newCurs)
define_new_tables(newCon,newCurs)

def main():
    port_tables(OLD_DB,newCon,newCurs)



if __name__== "__main__":
    main()
