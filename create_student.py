import pandas as pd
import numpy as np
import pyodbc


def create_student(name):
    x = name.replace(" ", "").lower()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE " + student)
    cursor.execute("CREATE LOGIN " + student +
                   " WITH PASSWORD = 'database', CHECK_POLICY = OFF, DEFAULT_DATABASE = " + student)

    cursor.execute("USE [" + student + "]CREATE USER " +
                   student + " FOR LOGIN " + student)
    cursor.execute(
        "USE [" + student + "] ALTER ROLE db_owner ADD MEMBER " + student)


# import the names from the csv; make sure that the file name is correct. In this case, it is 'course_roster.csv'
roster = pd.read_csv(r'course_roster.csv')
names = np.array(roster["Name"])

# make each name lower case and remove spaces
names_lst = []
for name in names:
    x = name.replace(" ", "").lower()
    names_lst.append(x)


# admin parameters to connect to sql (update username, password, and db name to access database)
driver = 'SQL Server'
server = 'stairway.usu.edu'
db = 'PUT DB NAME HERE'
username = 'PUT ADMIN USERNAME HERE'
password = 'PUT ADMIN PASSWORD HERE'


# connect to the server
conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (
    driver, server, db, username, password), autocommit=True)

# for each student, create a database and create a login
for student in names_lst:
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE " + student)
    cursor.execute("CREATE LOGIN " + student +
                   " WITH PASSWORD = 'database', CHECK_POLICY = OFF, DEFAULT_DATABASE = " + student)

    cursor.execute("USE [" + student + "]CREATE USER " +
                   student + " FOR LOGIN " + student)
    cursor.execute(
        "USE [" + student + "] ALTER ROLE db_owner ADD MEMBER " + student)
