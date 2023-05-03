#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:44:36 2023

@author: anitabaculima
"""
import sqlite3
import pandas as pd
import streamlit as st

# create a connection to the database
import sqlite3
import pandas as pd
import streamlit as st

# create a connection to the database
conn = sqlite3.connect('ecsel_database.db')
query = "SELECT Country, Acronym FROM countries"
df_countries = pd.read_sql(query, conn) 

conn.close()

country_dict = dict(zip(df_countries["Acronym"], df_countries["Country"]))

print(country_dict)

st.selectbox('Select a Country:',df_countries["Acronym"]) 

# 2.8 create a new dataframe of participants
conn = sqlite3.connect('ecsel_database.db')
new_participants = '''SELECT country, shortName, name, activityType, organizationURL, role, SUM(ecContribution) 
           FROM participants
           WHERE role = 'participant'
           GROUP BY country
           ORDER BY SUM(ecContribution) DESC'''
df_participants = pd.read_sql_query(new_participants, conn)

conn.close()
print(df_participants)

#2.9 Visualization of the new dataframe
st.dataframe(df_participants) 

#2.10  Generating a project coordinators dataframe

conn = sqlite3.connect('ecsel_database.db')
new_coordinators = '''SELECT country, shortName, name, projectAcronym, activityType, role 
           FROM participants
           WHERE role = 'coordinator'
           GROUP BY country
           ORDER BY shortName ASC'''
           
df_coordinators = pd.read_sql_query(new_coordinators, conn)
query = f'''SELECT country, shortName, name, projectAcronym, activityType, role 
           FROM participants
           WHERE role = 'coordinator' AND country = '{newP}'
           GROUP BY country
           ORDER'''
          
conn.close()

print(df_coordinators)

#2.11 Visualization of the project coordinators dataframe
st.dataframe(df_coordinators) 
                   








