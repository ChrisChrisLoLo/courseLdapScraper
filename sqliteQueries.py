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

def insertTerm(attrDict,connection,cursor):
    #print(attrDict)
    cursor.execute('''
        insert into terms values
        (?,?,?,?);
        ''',(
            attrDict["term"][0].decode('utf-8'),
            attrDict["termTitle"][0].decode('utf-8'),
            attrDict["startDate"][0].decode('utf-8'),
            attrDict["endDate"][0].decode('utf-8')
            ))


    connection.commit()
    return

def insertCourse(attrDict,connection,cursor):
    # print(attrDict)
    cursor.execute('''
        insert into courses values
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
        ''',(
            attrDict["term"][0].decode('utf-8'),
            attrDict["course"][0].decode('utf-8'),
            attrDict["subject"][0].decode('utf-8'),
            attrDict["subjectTitle"][0].decode('utf-8'),
            attrDict["catalog"][0].decode('utf-8'),
            attrDict["courseTitle"][0].decode('utf-8'),
            attrDict["courseDescription"][0].decode('utf-8'),
            attrDict["facultyCode"][0].decode('utf-8'),
            attrDict["faculty"][0].decode('utf-8'),
            attrDict["departmentCode"][0].decode('utf-8'),
            attrDict["department"][0].decode('utf-8'),
            attrDict["career"][0].decode('utf-8'),
            attrDict["units"][0].decode('utf-8'),
            attrDict["asString"][0].decode('utf-8'),
            ))


    connection.commit()
    return