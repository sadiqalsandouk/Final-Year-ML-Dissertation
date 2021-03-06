#import classes
import analytics
import system
#import libraries
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from PIL import Image
from matplotlib import pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns
sns.set_theme(style="whitegrid")
import plotly.express as px
import sqlite3
import hashlib
st.set_option('deprecation.showPyplotGlobalUse', False)


# security
#passlib,hashlib,bcrypt,scrypt

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False
# DB management

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def main():
    

    menu = ["Home","Login"]#,"Sign Up"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        image = Image.open('C:/Users/sadiq/OneDrive/Work/Uni/CS3605 Final Year Project/Resources/1.png')
        image2 = Image.open('C:/Users/sadiq/OneDrive/Work/Uni/CS3605 Final Year Project/Resources/2.png')
        st.image(image, use_column_width=True)
        st.image(image2, use_column_width=True)


    elif choice == "Login":
        st.sidebar.subheader("Login Section")
        st.title("Please login using the left sidebar")
        st.subheader("")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged in as {}".format(username))
                

                pagenav = st.selectbox("Page Navigation",["System","Analytics"])
                if pagenav == "Analytics":
                    analytics.main()
                    
                elif pagenav == "System":
                    system.main()
          
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Sign Up"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

main()