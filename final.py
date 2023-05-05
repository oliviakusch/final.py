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

print(df_countries)
country_names = dict(zip(df_countries["Country"], df_countries["Acronym"]))

print(country_names)

selectedcountry = st.selectbox('Select a Country:',list(country_names.keys()))   # new step get acronym given the country name 
selectedacronym = country_names[selectedcountry]


# 2.8 create a new dataframe of participants
conn = sqlite3.connect('ecsel_database.db')
new_participants = '''SELECT shortName, name, activityType, organizationURL, SUM(ecContribution) 
           FROM participants
           WHERE role = 'participant'AND 'country'='{}' 
           ORDER BY SUM(ecContribution) DESC'''

# df_participants = pd.read_sql_query(new_participants, conn)
df_participants = pd.read_sql_query("""SELECT shortName, name, activityType, organizationURL, SUM(ecContribution)  FROM participants WHERE country = '{}' GROUP BY ecContribution ORDER BY SUM(ecContribution)""".format(selectedacronym), conn)


conn.close()
print(df_participants)

#2.9 Visualization of the new dataframe
st.dataframe(df_participants) 

#2.10  Generating a project coordinators dataframe

conn = sqlite3.connect('ecsel_database.db')
new_coordinators = '''SELECT shortName, name, projectAcronym, activityType 
           FROM participants
           WHERE role = 'coordinator' AND 'country'='{}' 
           GROUP BY country
           ORDER BY shortName ASC'''

# df_coordinators = pd.read_sql_query(new_coordinators, conn)

df_coordinators = pd.read_sql_query("""SELECT * FROM participants WHERE role = 'coordinator' AND country = '{}' """.format(selectedacronym), conn)


conn.close()

print(df_coordinators)

#2.11 Visualization of the project coordinators dataframe
st.dataframe(df_coordinators) 
                   
