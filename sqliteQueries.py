import sqlite3

#Connect to db file
def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor

# Drop all tables in the given database
def drop_tables(connection, cursor):
    drop_query= '''
        PRAGMA foreign_keys = OFF;
        drop table if exists terms;
        drop table if exists courses;
        drop table if exists classes;
        drop table if exists classTimes;
        drop table if exists textbooks;
        PRAGMA foreign_keys = ON;
        '''
    cursor.executescript(drop_query)
    connection.commit()
    return


# Define and create tables in the given databse
def define_tables(connection, cursor):
    table_query = '''
        PRAGMA foreign_keys = ON;
        
        create table terms (
            term        char(4),
            termTitle   varchar(40),
            startDate   date,
            endDate     date,
            primary key (term)
        );

        create table courses (
            term                char(4),
            course              char(6),
            subject             char(6),
            subjectTitle        varchar(120),
            catalog             char(3),
            courseTitle         varchar(120),
            courseDescription   varchar(1600),
            facultyCode         char(2),
            faculty             varchar(60),
            departmentCode      char(10),
            department          varchar(100),
            career              varchar(10),
            units               decimal(3,2),
            asString            varchar(12),
            primary key (course),
            foreign key (term) references terms
        );

        create table classes (
            term            char(4),
            course          char(6),
            class           char(5),
            section         varchar(5),
            component       char(3),
            classType       char(1),
            classStatus     char(1),
            enrollStatus    char(1),
            capacity        int,
            startDate       date,
            endDate         date,
            session         varchar(33),
            campus          varchar(4),
            location        varchar(32),
            autoEnroll      varchar(5),
            classTopic      varchar(64),
            classNotes      varchar(400),
            consent         varchar(16),
            gradingBasis    varchar(16),
            instructionMode varchar(16),
            units           decimal(3,2),
            classURL        varchar(64),
            instructorUId   varchar(12),
            examStatus      varchar(9),
            examDate        date,
            examStartTime   char(8),
            examEndTime     char(8),
            examLocation    varchar(16),
            asString        varchar(32),
            primary key (class),
            foreign key (course) references courses,
            foreign key (term) references terms            
        );
        
        create table classTimes (
            term            char(4),
            course          char(6),
            class           char(5),
            classTime       varchar(8),
            day             char(7),
            startTime       char(8),
            endTime         char(9),
            location        varchar(16),
            endDate         date,
            startDate       date,
            primary key (classTime),
            foreign key (class) references class,
            foreign key (course) references courses,
            foreign key (term) references terms   
            
        );

        create table textbooks (
            term            char(4),
            course          char(6),
            class           char(5),
            textbook        varchar(16),
            uOfATxStatus    char(3),
            uOfATxTitle     varchar(64),
            uOfATxISBN      char(13),
            uOfATxAuthor    varchar(32),
            uOfATxPublisher varchar(32),
            uOfATxEdition   int,
            uOfATxYear      int,
            primary key (textbook),
            foreign key (class) references class,
            foreign key (course) references courses,
            foreign key (term) references terms   
        );
                    
        '''
    cursor.executescript(table_query)
    connection.commit()
    return

#Gets value from dictionary, and sets value to None if the optional parameter is set
def getVal(attrDict,key,optional=False):
    if optional:
        try:
            optionalVal = attrDict[key][0].decode('utf-8')
        except KeyError:
            optionalVal = None
        return optionalVal
    else:
       return attrDict[key][0].decode('utf-8')

def insertTerm(attrDict,connection,cursor):
    print(attrDict)
    cursor.execute('''
        insert into terms values
        (?,?,?,?);
        ''',(
            getVal(attrDict,"term"),
            getVal(attrDict,"termTitle"),
            getVal(attrDict,"startDate"),
            getVal(attrDict,"endDate")
            ))


    connection.commit()
    return



def insertCourse(attrDict,connection,cursor):
    print(attrDict)
    try:
        optCourseDesc = attrDict["courseDescription"][0].decode('utf-8')
    except KeyError:
        optCourseDesc = None

    cursor.execute('''
        insert or ignore into courses values
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        ''',(
            getVal(attrDict,"term"),
            getVal(attrDict,"course"),
            getVal(attrDict,"subject"),
            getVal(attrDict,"subjectTitle"),
            getVal(attrDict,"catalog"),
            getVal(attrDict,"courseTitle"),
            getVal(attrDict,"courseDescription",True),
            getVal(attrDict,"facultyCode"),
            getVal(attrDict,"faculty"),
            getVal(attrDict,"departmentCode"),
            getVal(attrDict,"department"),
            getVal(attrDict,"career"),
            getVal(attrDict,"units"),
            getVal(attrDict,"asString")
            ))


    connection.commit()
    return

def insertClass(attrDict,connection,cursor):
    print(attrDict)
    cursor.execute('''
        insert or ignore into classes values
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        ''',(
            getVal(attrDict,"term"),
            getVal(attrDict,"course"),
            getVal(attrDict,"class"),
            getVal(attrDict,"section"),
            getVal(attrDict,"component"),
            getVal(attrDict,"classType"),
            getVal(attrDict,"classStatus"),
            getVal(attrDict,"enrollStatus"),
            getVal(attrDict,"capacity"),
            getVal(attrDict,"startDate"),
            getVal(attrDict,"endDate"),
            getVal(attrDict,"session"),
            getVal(attrDict,"campus"),
            getVal(attrDict,"location"),
            getVal(attrDict,"autoEnroll",True),
            getVal(attrDict,"classTopic",True),
            getVal(attrDict,"classNotes",True),
            getVal(attrDict,"consent"),
            getVal(attrDict,"gradingBasis"),
            getVal(attrDict,"instructionMode"),
            getVal(attrDict,"units"),
            getVal(attrDict,"classURL",True),
            getVal(attrDict,"instructorUId",True),
            getVal(attrDict,"examStatus",True),
            getVal(attrDict,"examDate",True),
            getVal(attrDict,"examStartTime",True),
            getVal(attrDict,"examEndTime",True),
            getVal(attrDict,"examLocation",True),
            getVal(attrDict,"asString")
            ))
    connection.commit()
    return