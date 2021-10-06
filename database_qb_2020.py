import mysql.connector
import quarterbacks_script
import streamlit as st


def app():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="s2037940!!PP",
    database="nfl_stats"
    )
    mycursor = mydb.cursor()



    mycursor.execute("SELECT * FROM nfl_player_qb_search")

    myresult = mycursor.fetchall()


    for x in myresult:
        print(x)
