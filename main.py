import pandas as pd
import numpy as np
import pyodbc
import streamlit as st

st.title("Add Student Databases")

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


def callback():
    # Button was clicked
    st.session_state.button_clicked = True


# get the csv file from the user; get the student names from the csv file
st.write("You can get the Class Roster csv file by going to Canvas Course -> People -> Download Course Roster")
#class_roster = st.file_uploader("Upload the course roster csv file:")

# create a form
with st.form("my_form"):
    # get user parameters parameters to connect to SQL Server
    class_roster = st.file_uploader("Upload the course roster csv file:")
    st.write("Enter admin login information here:")
    server = st.text_input("Enter the server name:")
    db = st.text_input("Enter a database name (any database in the server):")
    username = st.text_input("Enter the admin username:")
    password = st.text_input("Enter the admin password:", type="password")
    submission = st.form_submit_button("Submit")
    if submission == True:
        st.success("Successfully submitted")

driver = 'SQL Server'
st.write("Only select this button if you have submitted the above form:")
if st.button("Make Student Databases/Logins", on_click=callback) or st.session_state.button_clicked:

    # make each name lower case and remove spaces
    roster = pd.read_csv(class_roster)
    names = np.array(roster["Name"])
    names_lst = []
    for name in names:
        x = name.replace(" ", "").lower()
        names_lst.append(x)

    # connect to the server
    conn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % (
        driver, server, db, username, password), autocommit=True)

    # for each student, create a database and create a login
    successfull_additions = []
    for student in names_lst:
        cursor = conn.cursor()
        try:
            cursor.execute("CREATE DATABASE " + student)
        except:
            st.write("Database already exists for " + student)
            continue
        cursor.execute("CREATE LOGIN " + student +
                       " WITH PASSWORD = 'database', CHECK_POLICY = OFF, DEFAULT_DATABASE = " + student)

        cursor.execute("USE [" + student + "]CREATE USER " +
                       student + " FOR LOGIN " + student)
        cursor.execute(
            "USE [" + student + "] ALTER ROLE db_owner ADD MEMBER " + student)
        successfull_additions.append(student)

    if len(successfull_additions) == 0:
        st.write("No students were added.")
    else:
        st.write(
            "The following databases and logins were successfully added: \n" + successfull_additions)
