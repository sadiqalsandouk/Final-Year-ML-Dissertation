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

def main():
    #get the data
    df = pd.read_csv('C:/Users/sadiq/OneDrive/Work/Uni/CS3605 Final Year Project/FYP/DATASET.csv', keep_default_na=False)
    #show the data in a table
    st.subheader('Data:')
    st.dataframe(df)
    #cleaning the data (Yes/No)
    df = df.replace(['', 'Unsure', 'Not applicable to me', 'No, I don\'t know any', 'Not eligible for coverage / N/A','No', 'Never', 'I don\'t know', 'I know some', 'Rarely', 'Often', 'Sometimes', 'Maybe', 'Yes', 'Yes, I know several', 'Always'], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    #cleaning the gender column does not reflect any views, I have attempted to be as aware as possible with the goal to make the models as optimal as possible.
    #cleaning the data (Gender - Male)
    df = df.replace(['Male', 'Dude', 'Male.', 'cisdude', 'I\'m a man why didn\'t you make this a drop down question. You should of asked sex? And I would of answered yes please. Seriously how much text can this take? ', 'male ', 'MALE' ,'Sex is male' ,'male', 'Male ', 'M', 'm', 'man', 'Male (cis)', 'cis man', 'cisdude' 'MALE', 'cis male', 'Cis Male', 'Cis male', 'Man', 'mail', 'Malr', 'M|'], 
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #cleaning the data (Gender - Female)
    df = df.replace(['Female', 'female', 'female ', 'Cis female ', ' Female', 'Female (props for making this a freeform field, though)', 'Female ', 'F', 'f', 'fem', 'woman', 'Woman', 'female/woman', 'Cis-woman', 'fm', 'I identify as female.' ], 
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    #cleaning the data (Gender - Other)
    df = df.replace(['non-binary', 'Nonbinary', 'N/A', 'Agender', 'genderqueer woman', 'Unicorn', 'Androgynous', 'Human', 'Fluid', 'Transitioned, M2F', 'AFAB', 'Enby', 'Female or Multi-Gender Femme', 'Other', 'mtf', 'Genderflux demi-girl', 'Other/Transfeminine', 'none of your business', 'nb masculine', 'genderqueer', 'human', 'Queer', 'Genderqueer', 'Bigender', 'Genderfluid', 'Genderfluid (born female)', 'Male (trans, FtM)', 'Transgender woman', 'Cisgender Female', 'Male/genderqueer', 'female-bodied; no feelings about gender', 'male 9:1 female, roughly', 'Female assigned at birth ' ], 
                        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    #cleaning the data (Age)
    df = df.replace([323], 
                        [30])
    #show the new data in a table

    st.subheader('Key:')
    st.write('0 = No | 1 = Yes')
    st.write('(Gender): 0 = M | 1 = F | 2 = Other')
    st.subheader('Clean Data:')
    st.dataframe(df)
    #show statistics on the data

    st.subheader('Stats:')
    st.write(df.describe())
    st.subheader('Mode:')
    st.write(df.mode())
    st.subheader('Median:')
    st.write(df.median())
    #show data as a chart

    st.subheader('Charts:')
    charts = st.bar_chart(df)
    st.subheader('Correlation Matrix:')
    #correlation matrix

    corrmat = df.corr()
    f, ax = plt.subplots(figsize=(12, 9))
    sns.heatmap(corrmat, vmax=.8, square=True)
    st.pyplot()
    st.subheader('Correlation Matrix (Treatment):')
    k = 10 #number of variables for heatmap

    cols = corrmat.nlargest(k, 'Have you ever sought treatment for a mental health issue from a mental health professional?')['Have you ever sought treatment for a mental health issue from a mental health professional?'].index
    cm = np.corrcoef(df[cols].values.T)
    sns.set(font_scale=1.25)
    hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
    st.pyplot()                    
    #distribution and desnsity by age / treatment or no treatment

    st.subheader('Distrubtion and Density by Age:')
    g = sns.FacetGrid(df, col='Have you ever sought treatment for a mental health issue from a mental health professional?', size=10)
    g = g.map(sns.distplot, "What is your age?")
    st.pyplot()
    #treatment from the age/gender point

    st.subheader('Treatment / Age & Gender:')
    data_age = df.loc[df['What is your age?']]
    fig = px.violin(data_age, y="What is your age?", x="Have you ever sought treatment for a mental health issue from a mental health professional?", color="What is your gender?", box=True, points="all")
    st.plotly_chart(fig)