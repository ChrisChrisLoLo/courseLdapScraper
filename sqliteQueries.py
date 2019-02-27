import sqlite3

#Connect to db file
def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
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
        PRAGMA foreign_keys = ON;
        '''
    cursor.executescript(drop_query)
    connection.commit()
    return


# Define and create tables in the given database
# NOTE: one big difference between this schema and the documentation schema is that 
# the classtime attribute does not appear to exist. This contradicts the documentation.
# The workaround is to give an autoincrementing int for an id, as it can be assumed that every
# classTime is unique
def define_tables(connection, cursor):
    table_query = '''
        PRAGMA foreign_keys = ON;
        
        create table terms (
            term        int,
            termTitle   varchar(40),
            startDate   date,
            endDate     date,
            primary key (term)
        );

        create table courses (
            term                int,
            course              int,
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
            class           INTEGER PRIMARY KEY AUTOINCREMENT,
            term            int,
            course          int,
            classCode       int,
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
            foreign key (course) references courses,
            foreign key (term) references terms            
        );
        
        create table classTimes (
            classTime       INTEGER PRIMARY KEY AUTOINCREMENT,
            term            int,
            course          int,
            class           int,
            day             char(7),
            startTime       char(8),
            endTime         char(9),
            location        varchar(16),
            endDate         date,
            startDate       date,
            foreign key (class) references classes,
            foreign key (course) references courses,
            foreign key (term) references terms   
            
        );
        '''
        # Too few textbook entries for data to be meaningful
        # create table textbooks (
        #     term            int,
        #     course          int,
        #     class           int,
        #     textbook        varchar(16),
        #     uOfATxStatus    char(3),
        #     uOfATxTitle     varchar(64),
        #     uOfATxISBN      char(13),
        #     uOfATxAuthor    varchar(32),
        #     uOfATxPublisher varchar(32),
        #     uOfATxEdition   int,
        #     uOfATxYear      int,
        #     primary key (textbook),
        #     foreign key (class) references classes,
        #     foreign key (course) references courses,
        #     foreign key (term) references terms   
        # );
                    
        # '''
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
            int(getVal(attrDict,"term")),
            int(getVal(attrDict,"course")),
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

#Classes are NOT unique, so a surrogate ID must be added.
def insertClass(attrDict,connection,cursor):
    print(attrDict)
    cursor.execute('''
        insert into classes values
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        ''',(
            None,   #Autoincrement surrogate ID.
            int(getVal(attrDict,"term")),
            int(getVal(attrDict,"course")),
            int(getVal(attrDict,"class")),
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

def insertClassTime(attrDict,connection,cursor):
    print(attrDict)

    #Find the surrogate class ID that matches the given
    #term, course, and classCode, since classCodes are not unique
    cursor.execute('''select * 
                    from classes
                    where term = (?)
                    and course = (?)
                    and classCode = (?);
                    ''',(
                        int(getVal(attrDict,"term")),
                        int(getVal(attrDict,"course")),
                        int(getVal(attrDict,"class")),
                    ))

    classMatch = cursor.fetchone()

    cursor.execute('''
        insert into classTimes values
        (?,?,?,?,?,?,?,?,?,?);
        ''',(
            None,   #Use an auto incrementing id
            int(getVal(attrDict,"term")),
            int(getVal(attrDict,"course")),
            int(classMatch["class"]),
            getVal(attrDict,"day"),
            getVal(attrDict,"startTime"),
            getVal(attrDict,"endTime"),
            getVal(attrDict,"location",True),
            getVal(attrDict,"endDate"),
            getVal(attrDict,"startDate"),
        ))
    connection.commit()
    return

# def insertTextbook(attrDict,connection,cursor):
#     print(attrDict)
#     cursor.execute('''
#         insert into textbooks values
#         (?,?,?,?,?,?,?,?,?,?,?)
#         ''',(
#             int(getVal(attrDict,"term")),
#             int(getVal(attrDict,"course")),
#             int(getVal(attrDict,"class")),
#             getVal(attrDict,"textbook"),
#             getVal(attrDict,"uOfATxStatus",True),
#             getVal(attrDict,"uOfATxTitle",True),
#             getVal(attrDict,"uOfATxISBN",True),
#             getVal(attrDict,"uOfATxAuthor",True),
#             getVal(attrDict,"uOfATxPublisher",True),
#             getVal(attrDict,"uOfATxEdition",True),
#             getVal(attrDict,"uOfATxYear",True),
#         ))
#     connection.commit()
#     return