import sqlite3
import pandas as pd
import streamlit as st

# create a connection to the database
import sqlite3
import pandas as pd
import streamlit as st

from PIL import Image
image = Image.open('image2.jpg') # Load the image from disk
st.image(image) # Display the image
st.title(":green[_Partner Search_]")

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


selectedcountry = st.selectbox('Select a Country :earth_africa: :',list(country_names.keys())) 
selectedacronym = country_names[selectedcountry]

st.caption("_You have selected:_ " + :red[_selectedcountry_)

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
df_participants.to_csv('participants.csv')

#2.9 Visualization of the new dataframe
st.header('Participants in ' + selectedcountry)
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
df_coordinators.to_csv('project coordinators.csv')

#2.11 Visualization of the project coordinators dataframe
st.header('Coordinators in ' + selectedcountry)
st.dataframe(df_coordinators) 

#2.12 CSV Participant & Coordinators Download Button
df_participants = pd.read_csv("participants.csv")

def convert_df_participants(df):
   return df.to_csv(index=False).encode('utf-8')

participants_csv = convert_df_participants(df_participants)

st.download_button(
   label="Download Participants Database (.csv)",
   data=participants_csv,
   file_name="participants.csv",
   mime="text/csv;charset=utf-8",
   key='download-csv'
)

df_coordinators = pd.read_csv("project coordinators.csv")

def convert_df_coordinators(df):
   return df.to_csv(index=False).encode('utf-8')

coordinators_csv = convert_df_coordinators(df_coordinators)

st.download_button(
   label="Download Project Coordinators Database (.csv)",
   data= coordinators_csv,
   file_name="project coordinators.csv",
   mime="text/csv;charset=utf-8",
   key='download1-csv'
)

#Added Functionalities
conn = sqlite3.connect('ecsel_database.db')
df_chart = pd.read_sql_query("""SELECT activityType, country, SUM(ecContribution) FROM participants WHERE country = '{}' GROUP BY activityType""".format(selectedacronym), conn)

conn.close()
df_chart = df_chart.rename(columns=columnnamechanges)
print(df_chart)

st.dataframe(df_chart) 

st.bar_chart(data=df_chart, x='activityType', y='SUM(ecContribution)')

