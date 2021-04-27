import sqlite3

#Connect to db file
def connect(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return connection, cursor

# Drop all tables in the given database
def drop_new_tables(connection, cursor):
    dropQuery= '''
        PRAGMA foreign_keys = OFF;
        drop table if exists faculties;
        drop table if exists departments;
        drop table if exists subjects;
        drop table if exists terms;
        drop table if exists courses;
        drop table if exists classes;
        drop table if exists classTimes;
        drop table if exists textbooks;
        PRAGMA foreign_keys = ON;
        '''
    cursor.executescript(dropQuery)
    connection.commit()
    return


# Define and create tables in the given database
# NOTE: These tables are as split up as much as they logically make sense to
# cut down on duplication. However, since the data is pretty stable (no edits needed),
# data redundency may matter less, and joining multiple tables (faculties, departments, subjects)
# might make more sense for performance
def define_new_tables(connection, cursor):

    cursor.execute('''PRAGMA foreign_keys = ON;''')

    cursor.execute('''
        
        
        create table faculties (
            facultyCode         char(2),
            faculty             varchar(60),
            primary key (facultyCode)
        );
        '''
    )

    cursor.execute('''
        create table departments (
            departmentCode      char(10),
            department          varchar(100),
            facultyCode         char(2),
            primary key (departmentCode),
            foreign key (facultyCode) references faculties
        );
        '''
    )

    cursor.execute('''
        create table subjects (
            subject             char(6),
            subjectTitle        varchar(120),
            departmentCode      char(10),
            primary key (subject),
            foreign key (departmentCode) references departments
        );
        '''
    )

    cursor.execute('''
        create table courses (
            course              int,
            catalog             char(3),
            courseTitle         varchar(120),
            courseDescription   varchar(1600),
            career              varchar(10),
            units               decimal(3,2),
            asString            varchar(12),
            subject             char(6),
            primary key (course),
            foreign key (subject) references subjects
        );
        '''
    )

    cursor.execute('''
        create table terms (
            term        int,
            termTitle   varchar(40),
            startDate   date,
            endDate     date,
            primary key (term)
        );
        '''
    )

    cursor.execute('''
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
        '''
    )

    cursor.execute('''
        create table classTimes (
            classTime       INTEGER PRIMARY KEY AUTOINCREMENT,
            class           int,
            day             char(7),
            startTime       char(8),
            endTime         char(9),
            location        varchar(16),
            endDate         date,
            startDate       date,
            foreign key (class) references classes
        );
        '''
    )

    cursor.execute('''
        create table textbooks (
            class           int,
            textbook        varchar(16),
            uOfATxStatus    char(3),
            uOfATxTitle     varchar(64),
            uOfATxISBN      char(13),
            uOfATxAuthor    varchar(32),
            uOfATxPublisher varchar(32),
            uOfATxEdition   int,
            uOfATxYear      int,
            primary key (textbook),
            foreign key (class) references classes
        );
        '''
    )
    connection.commit()

    return

def port_tables(oldDBPath,newCon,newCurs):
    print(oldDBPath)
    #Connect the old database to the new one and 
    newCurs.execute('''
        ATTACH DATABASE (?) AS old;
        ''',(oldDBPath,))

    #Break up courses into smaller tables
    newCurs.execute('''
        INSERT OR IGNORE INTO faculties
        SELECT facultyCode,faculty
        FROM old.courses;
        ''')

    newCurs.execute('''
        INSERT OR IGNORE INTO departments
        SELECT departmentCode,department,facultyCode
        FROM old.courses;
        ''')
    
    newCurs.execute('''
        INSERT OR IGNORE INTO subjects
        SELECT subject,subjectTitle,departmentCode
        FROM old.courses;
        ''')
    
    newCurs.execute('''
        INSERT OR IGNORE INTO courses
        SELECT course,
            catalog,
            courseTitle,
            courseDescription,
            career,
            units,
            asString,
            subject
        FROM old.courses;
        ''')

    #Port other tables relatively unaltered (removed some unessicary FKs)
    newCurs.execute('''
        INSERT INTO terms
        SELECT *
        FROM old.terms;
        ''')

    newCurs.execute('''
        INSERT INTO classes
        SELECT *
        FROM old.classes
        ''')

    newCurs.execute('''
        INSERT INTO classTimes
        SELECT
            classTime,
            class,
            day,
            startTime,
            endTime,
            location,
            endDate,
            startDate
        FROM old.classTimes;
        ''')

    # newCurs.execute('''
    #     INSERT INTO textbooks
    #     SELECT
    #         class,
    #         textbook,
    #         uOfATxStatus,
    #         uOfATxTitle,
    #         uOfATxISBN,
    #         uOfATxAuthor,
    #         uOfATxPublisher,
    #         uOfATxEdition,
    #         uOfATxYear
    #     FROM old.textbooks;
    #     ''')
    newCon.commit()
    return

#Gets value from dictionary, and sets value to None if the optional parameter is set
# def getVal(attrDict,key,optional=False):
#     if optional:
#         try:
#             optionalVal = attrDict[key][0].decode('utf-8')
#         except KeyError:
#             optionalVal = None
#         return optionalVal
#     else:
#        return attrDict[key][0].decode('utf-8')

# def insertTerm(attrDict,connection,cursor):
#     print(attrDict)
#     cursor.execute('''
#         insert into terms values
#         (?,?,?,?);
#         ''',(
#             getVal(attrDict,"term"),
#             getVal(attrDict,"termTitle"),
#             getVal(attrDict,"startDate"),
#             getVal(attrDict,"endDate")
#             ))


#     connection.commit()
#     return



# def insertCourse(attrDict,connection,cursor):
#     print(attrDict)
#     try:
#         optCourseDesc = attrDict["courseDescription"][0].decode('utf-8')
#     except KeyError:
#         optCourseDesc = None

#     cursor.execute('''
#         insert or ignore into courses values
#         (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
#         ''',(
#             int(getVal(attrDict,"term")),
#             int(getVal(attrDict,"course")),
#             getVal(attrDict,"subject"),
#             getVal(attrDict,"subjectTitle"),
#             getVal(attrDict,"catalog"),
#             getVal(attrDict,"courseTitle"),
#             getVal(attrDict,"courseDescription",True),
#             getVal(attrDict,"facultyCode"),
#             getVal(attrDict,"faculty"),
#             getVal(attrDict,"departmentCode"),
#             getVal(attrDict,"department"),
#             getVal(attrDict,"career"),
#             getVal(attrDict,"units"),
#             getVal(attrDict,"asString")
#             ))


#     connection.commit()
#     return

# def insertClass(attrDict,connection,cursor):
#     print(attrDict)
#     cursor.execute('''
#         insert or ignore into classes values
#         (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
#         ''',(
#             int(getVal(attrDict,"term")),
#             int(getVal(attrDict,"course")),
#             int(getVal(attrDict,"class")),
#             getVal(attrDict,"section"),
#             getVal(attrDict,"component"),
#             getVal(attrDict,"classType"),
#             getVal(attrDict,"classStatus"),
#             getVal(attrDict,"enrollStatus"),
#             getVal(attrDict,"capacity"),
#             getVal(attrDict,"startDate"),
#             getVal(attrDict,"endDate"),
#             getVal(attrDict,"session"),
#             getVal(attrDict,"campus"),
#             getVal(attrDict,"location"),
#             getVal(attrDict,"autoEnroll",True),
#             getVal(attrDict,"classTopic",True),
#             getVal(attrDict,"classNotes",True),
#             getVal(attrDict,"consent"),
#             getVal(attrDict,"gradingBasis"),
#             getVal(attrDict,"instructionMode"),
#             getVal(attrDict,"units"),
#             getVal(attrDict,"classURL",True),
#             getVal(attrDict,"instructorUId",True),
#             getVal(attrDict,"examStatus",True),
#             getVal(attrDict,"examDate",True),
#             getVal(attrDict,"examStartTime",True),
#             getVal(attrDict,"examEndTime",True),
#             getVal(attrDict,"examLocation",True),
#             getVal(attrDict,"asString")
#             ))
#     connection.commit()
#     return

# def insertClassTime(attrDict,connection,cursor):
#     print(attrDict)
#     cursor.execute('''
#         insert or ignore into classTimes values
#         (?,?,?,?,?,?,?,?,?,?)
#         ''',(
#             None,               #Use an auto incrementing id
#             int(getVal(attrDict,"term")),
#             int(getVal(attrDict,"course")),
#             int(getVal(attrDict,"class")),
#             getVal(attrDict,"day"),
#             getVal(attrDict,"startTime"),
#             getVal(attrDict,"endTime"),
#             getVal(attrDict,"location",True),
#             getVal(attrDict,"endDate"),
#             getVal(attrDict,"startDate"),
#         ))
#     connection.commit()
#     return

# def insertTextbook(attrDict,connection,cursor):
#     print(attrDict)
#     cursor.execute('''
#         insert or ignore into textbooks values
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