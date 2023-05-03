#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:42:43 2023

@author: oliviakusch
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### FR 1.1: Read the 3 previous EXCEL files
project = pd.read_excel("projects.xlsx")
participants = pd.read_excel("participants.xlsx")
countries = pd.read_excel("countries.xlsx")

### FR 1.2: Display a bar plot with the total annual received grants
def annual_grants():
    global data
    data = project.groupby('year').agg(sum)['ecMaxContribution']
    years = data.index.values
    grants = list(data.values)
    print("Years", years)
    print("Grants", grants)
    return grants

#if __name__ == '__main__'


annual_grants()
grants_plot=data.plot.bar()

### FR 1.3: Generate descriptive statistics
### FR 1.4: Visualize the generated descriptive statistics
stats = data.describe()
print(stats)


### FR 1.5
country_acronyms = {'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany': 'DE', 
                    'Estonia': 'EE', 'Ireland': 'IE','Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 'Croatia': 'HR', 
                    'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT','Luxembourg': 'LU', 
                    'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 
                    'Portugal': 'PT','Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 'Finland': 'FI', 
                    'Sweden': 'SE'}

# country input & validate 
while True:
    country_name = input('Enter a country name: ')
    if country_name not in country_acronyms:
        print('Invalid country name. Please try again.')
    else:
        break
country_code = country_acronyms[country_name]

### FR 1.6
filtered_data = participants[participants['country'] == country_code]

aggregated_data = filtered_data.groupby(['shortName', 'name', 'activityType', 'organizationURL']).agg(
    count_project=('projectID', 'count'),
    sum_ecContribution=('ecContribution', 'sum')
).reset_index()   

### FR 1.7: Display in screen the generated dataset, in descending order by received grants
sorted_data = aggregated_data.sort_values('sum_ecContribution', ascending=False)
print("\nGenerated Dataset:")
print(sorted_data)


### FR 1.8: Save the generated dataset (received grants per partner) in an EXCEL file
output_file = "output_partner.xlsx"
### sorted_data.to_excel(output_file, index=False)
### ^^ commented becayse it writes a new excel file every time it runs
print(f"\nThe dataset has been saved as '{output_file}'.")


###

###