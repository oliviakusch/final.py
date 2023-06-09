import sqlite3
import pandas as pd
import streamlit as st


# import image to streamlit
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

# create country dictionary for use of the dropdown box
country_names = dict(zip(df_countries["Country"], df_countries["Acronym"]))
print(country_names)

# creating country drop box
selectedcountry = st.selectbox('Select a Country :earth_africa: :',list(country_names.keys())) 
selectedacronym = country_names[selectedcountry]

st.caption(f"You have selected: **{selectedcountry}**")

# 2.8 create a new dataframe of participants
conn = sqlite3.connect('ecsel_database.db')
df_participants = pd.read_sql_query("""SELECT shortName, name, activityType, organizationURL, SUM(ecContribution)  
FROM participants WHERE country = '{}' AND role = 'participant' 
GROUP BY ecContribution ORDER BY SUM(ecContribution) DESC""".format(selectedacronym), conn)

conn.close()

df_participants = df_participants.rename(columns=columnnamechanges)
print(df_participants)

df_participants.to_csv('participants.csv')

#2.9 Visualization of the new dataframe
st.header('Participants in ' + selectedcountry)
st.dataframe(df_participants) 

#2.10  Generating a project coordinators dataframe
conn = sqlite3.connect('ecsel_database.db')
df_coordinators = pd.read_sql_query("""SELECT * FROM participants 
WHERE country = '{}'AND role = 'coordinator' 
ORDER BY shortName ASC""".format(selectedacronym), conn)

conn.close()

# creating name changes for columns in the data frame 
df_coordinators = df_coordinators.rename(columns=columnnamechanges)

print(df_coordinators)
df_coordinators.to_csv('project coordinators.csv')

#2.11 Visualization of the project coordinators dataframe
st.header('Coordinators in ' + selectedcountry)
st.dataframe(df_coordinators) 


# Bar chart additional functionality
conn = sqlite3.connect('ecsel_database.db')
df_chart = pd.read_sql_query("""SELECT activityType, country, SUM(ecContribution) FROM participants WHERE country = '{}' GROUP BY activityType""".format(selectedacronym), conn)

conn.close()
df_chart = df_chart.rename(columns=columnnamechanges)
print(df_chart)

st.header('Evolution of Contribution Sum by Activity Type')
st.bar_chart(data=df_chart, x='Activity Type', y='Contribution Sum')
st.dataframe(df_chart)
  
  
  
# Keyword search additional functionality 

projects_dict = { 
    'MATQu': 'computing, technology, qubit', 
    'HELoS': 'initiative, medical, device, technology', 
    'AFarCloud': 'farming, labour, health, order, project', 
    'ASTONISH': 'application, imaging, technology', 
    'EXIST': 'image, sensor, imaging, pixel, high, filter, spectral', 
    'CSA-Industry4.E': 'liase, stakeholder, project', 
    'DENSE': 'system, weather, environment', 
    'Productive4.0': 'project, industry, solution', 
    'ENABLE-S3': 'system, test, validation', 
    'MANTIS': 'mantis, maintenance, system', 
    'POSITION-II': 'position, technology, platform', 
    'Moore4Medical': 'medical, application, technology, platform', 
    'TRANSACT': 'safety, critical, system, service, transact, cloud', 
    'InSecTT': 'thing, intelligent, secure, system', 
    'InForMed': 'pilot, line, fabrication', 
    'SCOTT': 'wireless, solution, end, domain, user', 
    'MegaMaRt2': 'productivity, industrial, runtime', 
    'DELPHI4LED': 'industry, product, market, multi, model, development, tool, compact', 
    '3Ccar': 'project, complexity, semiconductor, innovation', 
    'PRYSTINE': 'system, fail, operational, fusion', 
    'RobustSENSE': 'system, condition, robustsense', 
    'EuroPAT-MASIP': '', 
    'NewControl': 'platform, perception, control, safety', 
    'IMOCO4.E': 'machine, layer, control', 
    'FRACTAL': 'computing, node, cognitive', 
    'SECREDAS': 'title, security, cross, domain, reliable, dependable, multi, methodology, reference, architecture, component, autonomous, system, high, privacy, protection, functional, safety, operational, performance', 
    'AutoDrive': 'driving, european, system, autodrive, situation, safe', 
    'NextPerception': 'smart, system, health, wellbeing, solution, project, automotive, intelligence, monitoring', 
    'StorAIge': 'technology, high, performance, power, solution, application', 
    'REACTION': 'sic, line, power, smart', 
    'AI4DI': 'industry, ai, system', 
    'Arrowhead Tools': 'digitalisation, automation, tool, engineering', 
    'WInSiC4AP': 'technology, application, tier1', 
    'iRel40': 'reliability, system, application', 
    'R3-PowerUP': 'mm, pilot, line, smart, power', 
    'Energy ECS': 'energy, technology, new', 
    'PROGRESSUS': 'smart, grid, infrastructure, power, station, energy', 
    'BEYOND5': 'radio, technology, soi, pilot', 
    'YESvGaN': 'yesvgan, low, cost, power, transistor, technology'}
  
def get_projects_by_keyword(keywords, projects_dict):
    projects = []
    for project, project_keywords in projects_dict.items():
        if all(keyword in project_keywords for keyword in keywords):
            projects.append(project)
    return projects
  
# enter in streamlit
def main():
    st.title("Search Projects By Keyword:")
    
# code for splitting the list of values in the key value pairs
    all_keywords = [keyword for keywords in projects_dict.values() for keyword in keywords.split(", ")]
    unique_keywords = list(set(all_keywords))

    keyword = st.multiselect("Select at least one keyword", unique_keywords)

    if st.button("Search"):
        if keyword:
            projects = get_projects_by_keyword(keyword, projects_dict)
            if projects:
                st.success(f"Projects related to these keywords: '{keyword}':")
                for project in projects:
                    st.write(f"- {project}")
            else:
                st.warning("No projects found for this keyword or combination of keywords.")
        else:
            st.warning("Please enter at least one keyword.")

if __name__ == "__main__":
    main()
  
  
# 2.12 CSV Participant & Coordinators Download Button
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
