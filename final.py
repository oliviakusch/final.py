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

st.caption(f"You have selected: **{selectedcountry}**")

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


#Added Functionalities
conn = sqlite3.connect('ecsel_database.db')
df_chart = pd.read_sql_query("""SELECT activityType, country, SUM(ecContribution) FROM participants WHERE country = '{}' GROUP BY activityType""".format(selectedacronym), conn)

conn.close()
df_chart = df_chart.rename(columns=columnnamechanges)
print(df_chart)

st.header('Evolution of Contribution Sum by Activity Type')
st.bar_chart(data=df_chart, x='Activity Type', y='Contribution Sum')
st.dataframe(df_chart) 
             
  
def acronym_function(x):
    d = {'MATQu': 'computing, technology, qubit', 'HELoS': 'initiative, medical, device, technology', 
     'AFarCloud': 'farming, labour, health, order, project', 'ASTONISH': 'application, imaging, technology', 
     'EXIST': 'image, sensor, imaging, pixel, high, filter, spectral', 'CSA-Industry4.E': 'liase, stakeholder, project', 
     'DENSE': 'system, weather, environment', 'Productive4.0': 'project, industry, solution', 
     'ENABLE-S3': 'system, test, validation', 'MANTIS': 'mantis, maintenance, system', 
     'POSITION-II': 'position, technology, platform', 'Moore4Medical': 'medical, application, technology, platform', 
     'TRANSACT': 'safety, critical, system, service, transact, cloud', 'InSecTT': 'thing, intelligent, secure, system', 
     'InForMed': 'pilot, line, fabrication', 'SCOTT': 'wireless, solution, end, domain, user', 
     'MegaMaRt2': 'productivity, industrial, runtime', 'DELPHI4LED': 'industry, product, market, multi, model, development, tool, compact', 
     '3Ccar': 'project, complexity, semiconductor, innovation', 'PRYSTINE': 'system, fail, operational, fusion', 
     'RobustSENSE': 'system, condition, robustsense', 'EuroPAT-MASIP': '', 'NewControl': 'platform, perception, control, safety', 
     'IMOCO4.E': 'machine, layer, control', 'FRACTAL': 'computing, node, cognitive', 
     'SECREDAS': 'title, security, cross, domain, reliable, dependable, multi, methodology, reference, architecture, component, autonomous, system, high, privacy, protection, functional, safety, operational, performance', 'AutoDrive': 'driving, european, system, autodrive, situation, safe', 
     'NextPerception': 'smart, system, health, wellbeing, solution, project, automotive, intelligence, monitoring', 
     'StorAIge': 'technology, high, performance, power, solution, application', 'REACTION': 'sic, line, power, smart', 
     'AI4DI': 'industry, ai, system', 'Arrowhead Tools': 'digitalisation, automation, tool, engineering', 
     'WInSiC4AP': 'technology, application, tier1', 'iRel40': 'reliability, system, application', 'R3-PowerUP': 'mm, pilot, line, smart, power', 
     'Energy ECS': 'energy, technology, new', 'PROGRESSUS': 'smart, grid, infrastructure, power, station, energy', 
     'BEYOND5': 'radio, technology, soi, pilot', 'YESvGaN': 'yesvgan, low, cost, power, transistor, technology, vertical', 
     'ADACORSA': 'drone, technology, system', 'CONNECT': 'power, energy, grid, order, local', 'GaN4AP': 'gan, power, device', 
     'DAIS': 'new, component, project', 'ArchitectECA2030': 'validation, eca, vehicle, residual, risk', 
     'CHARM': 'manufacturing, industry, technology, sensor', 'COMP4DRONES': 'drone, ecosystem, comp4drone, architecture, application, compositional, platform', 
     'AI-TWILIGHT': 'lighting, product, digital, twin, ai', 'IoSense': 'manufacturing, market, line, sensor', 
     'PIN3S': 'semiconductor, technology, equipment, material', 'AI4CSM': 'mobility, automotive, industry, transition, digital, vehicle',
     'SILENSE': 'smart, acoustic, technology', 'Power2Power': 'power2power, innovation, power, smart, energy, application, key', 
     'MADEin4': 'metrology, productivity, industry, booster, major, challenge', 'FITOPTIVIS': 'objective, low, optimisation', 
     'SC3': 'semiconductor, supply, domain', 'ANDANTE': 'hardware, capability, application', 
     'COSMOS': 'project, ecsel, lighthouse, stakeholder', 'TAKEMI5': 'project, metrology, process, tool', 
     'OSIRIS': 'sic, power, substrate', 'PRIME': 'project, power, technology, design, block, system, iot', 
     'ID2PPAC': 'project, technology, nm, node, device', 'TAPES3': 'project, metrology, device', 
     'TAKE5': 'project, nm, technology, process', 'PowerBase': 'pilot, line, project', 'SeNaTe': 'nm, technology, process', 
     'ADMONT': 'pilot, line, technology, process, smart', 'MICROPRINCE': 'pilot, line, functional, component, technology', 
     'WAKeMeUP': 'project, memory, application, technology', 'APPLAUSE': 'advanced, packaging, manufacturing', 
     'SafeCOP': 'system, wireless, certification', 'TRANSFORM': 'energy, technology, process, new', 
     'SWARMs': 'offshore, vehicle, auvs, rovs', 'WAYTOGO FAST': 'project, technology, fdsoi, nm', 
     'AMASS': 'system, assurance, certification', 'AIDOaRt': 'continuous, development, software', 
     'CPS4EU': 'cps, technology, strategic, industry, european, large', 'IT2': 'project, technology, equipment, system', 
     'VALU3S': 'manufacturer, system, domain, v&v, method, tool', 'iDev40': 'development, process, manufacturing, digital, technology', 
     '5G_GaN2': 'technology, mm, wave', 'AQUAS': 'complexity, system, world, safety, security, performance, industrial', 
     'HiEFFICIENT': 'partner, high, level, system', 'HELIAUS': 'perception, system, thermal', 
     'SemI40': 'electronic, manufacturing, semi40, industry, partner, system', 'EnSO': 'energy, objective, smart', 
     'I-MECH': 'mech, system, motion, speed, control', 'HiPERFORM': 'high, semiconductor, power', 
     '3DAM': 'project, new, metrology, semiconductor, technology', 'VIZTA': 'technology, sensor, source, range, key, smart, filter, integrated', 
     'UltimateGaN': 'power, application, gan, device, efficiency', 'BRAINE': 'edge, computing, braine', 
     'R2POWER300': 'manufacturing, line, mm, new, process, technology, smart, power', 'REFERENCE': 'european, rf, technology', 
     'TARANTO': 'project, high, system', 'TEMPO': 'neuromorphic, dnn, technology', 'OCEAN12': 'fdsoi, technology, low'}
    return d[x]


# Streamlit app code
def main():
    st.title("Project Keyword Search")

    keyword = st.text_input("Enter a keyword")

    if st.button("Search"):
        if keyword:
            if keyword in d:
                projects = d[keyword]
                st.success(f"Projects for keyword '{keyword}':")
                for project in projects.split(', '):
                    st.write(f"- {project}")
            else:
                st.warning("Keyword not found.")
        else:
            st.warning("Please enter a keyword.")

if __name__ == "__main__":
    main()
  
  
  
  
  
  
  
###### 2.12 CSV Participant & Coordinators Download Button
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
