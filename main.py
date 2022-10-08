import pandas as pd
import numpy as np
import pyodbc
import streamlit as st


st.title("Add Student Databases")
driver = 'SQL Server'

c1 = st.container()
c2 = st.container()

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


def callback():
    # Button was clicked
    st.session_state.button_clicked = True


# get the csv file from the user; get the student names from the csv file
# class_roster = st.file_uploader("Upload the course roster csv file:")

# create a form
with c1.form("my_form"):
    # get user parameters parameters to connect to SQL Server
    st.write("You can get the Class Roster csv file by going to Canvas Course -> People -> Download Course Roster.")
    class_roster = st.file_uploader(
        "Upload the course roster csv file:")
    st.write("Enter admin login information here:")
    server = st.text_input("Enter the server name:")
    username = st.text_input("Enter the admin username:")
    password = st.text_input("Enter the admin password:", type="password")
    submission = st.form_submit_button("Submit and Run")
    if submission == True:
        try:
            roster = pd.read_csv(class_roster)
        except:
            st.error(
                "Error: Please attach the Class Roster csv file. This can be downloaded from Canvas.")
            st.stop()
        names = np.array(roster["Name"])
        names_lst = []
        for name in names:
            x = name.replace(" ", "").lower()
            names_lst.append(x)

        if server == "":
            st.warning("Please add a server name.")
            st.stop()

        if username == "":
            st.warning("Please add the admin username.")
            st.stop()

        if password == "":
            st.warning("Please add the admin password.")
            st.stop()

        # connect to the server
        try:
            conn = pyodbc.connect('driver={%s};server=%s;uid=%s;pwd=%s' % (
                driver, server,  username, password), autocommit=True)
        except:
            st.error(
                "Could not connect to SQL server. One or more of the form inputs is incorrect.")
            st.stop()

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
        st.success("Successfully submitted")
        if len(successfull_additions) == 0:
            st.warning("Result: No students were added.")
        else:
            st.subheader(
                "Result - The following databases and logins were successfully created:")
            for i in successfull_additions:
                st.success("\t" + str(i))
