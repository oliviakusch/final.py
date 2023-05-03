#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 19:53:44 2023

@author: oliviakusch
"""
import pandas as pd
from sqlite3 import connect

### FR2.1 
### The system shall read the 3 previous EXCEL files and generate 3 dataframes corresponding to the EXCEL tables

projects = pd.read_excel("projects.xlsx")
participants = pd.read_excel("participants.xlsx")
countries = pd.read_excel("countries.xlsx")

connection = connect("ecsel_database.db")

df_projects = pd.DataFrame(projects)
df_participants = pd.DataFrame(participants)
df_countries = pd.DataFrame(countries)

df_projects.to_sql("projects", connection, if_exists = "replace")
df_participants.to_sql("participants", connection, if_exists = "replace")
df_countries.to_sql("countries", connection, if_exists = "replace")

connection.close()

