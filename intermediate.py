#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:43:19 2023

@author: oliviakusch
"""
import sqlite3
import pandas as pd

### FR 2.5 The notebook shall connect to the ecsel_database.db and extract 
### the list of countries in a dataframe

connection = sqlite3.connect("ecsel_database.db")

df_countries = pd.read_sql_query("SELECT * FROM countries", connection)

connection.close()

print(df_countries) 