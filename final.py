import sqlite3
import pandas as pd
import streamlit as st

# create a connection to the database
import sqlite3
import pandas as pd
import streamlit as st

st.title("Partner Search")

# create a connection to the database
conn = sqlite3.connect('ecsel_database.db')

columnnamechanges = {"index" : "Index", "projectID" : "Project ID", "projectAcronym" : "Project Acronym",
                     "organisationID" : "Organization ID", "shortName" : "Short Name", "name" : "Name", 
                     "activityType" : "Activity Type", "organizationURL" : "Organization URL",  
                     "SUM(ecContribution)" : "Contribution Sum", "country" : "Country", "role" : "Role", "ecContribution" : "Contribution" }

query = "SELECT Country, Acronym FROM countries"
df_countries = pd.read_sql(query, conn) 

conn.close()


print(df_countries)

country_names = dict(zip(df_countries["Country"], df_countries["Acronym"]))

print(country_names)


selectedcountry = st.selectbox('Select a Country:',list(country_names.keys())) 
selectedacronym = country_names[selectedcountry]


# 2.8 create a new dataframe of participants
conn = sqlite3.connect('ecsel_database.db')
new_participants = '''SELECT shortName, name, activityType, organizationURL, SUM(ecContribution) 
           FROM participants
           WHERE role = 'participant'AND 'country'='{}' 
           ORDER BY SUM(ecContribution) DESC'''

# df_participants = pd.read_sql_query(new_participants, conn)
df_participants = pd.read_sql_query("""SELECT shortName, name, activityType, organizationURL, SUM(ecContribution)  FROM participants WHERE country = '{}' AND role = 'participant' GROUP BY ecContribution ORDER BY SUM(ecContribution)""".format(selectedacronym), conn)

conn.close()
print(df_participants)
df_participants = df_participants.rename(columns=columnnamechanges)

#2.9 Visualization of the new dataframe
st.header("Participants in", selectedacronym)
st.dataframe(df_participants) 

#2.10  Generating a project coordinators dataframe

conn = sqlite3.connect('ecsel_database.db')
new_coordinators = '''SELECT shortName, name, projectAcronym, activityType 
           FROM participants
           WHERE role = 'coordinator' AND 'country'='{}' 
           GROUP BY country
           ORDER BY shortName ASC'''

# df_coordinators = pd.read_sql_query(new_coordinators, conn)

df_coordinators = pd.read_sql_query("""SELECT * FROM participants WHERE country = '{}'AND role = 'coordinator' ORDER BY shortName ASC""".format(selectedacronym), conn)


conn.close()

df_coordinators = df_coordinators.rename(columns=columnnamechanges)

print(df_coordinators)

#2.11 Visualization of the project coordinators dataframe
st.dataframe(df_coordinators) 
                   
