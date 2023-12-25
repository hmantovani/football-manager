import pandas as pd
import numpy as np
import os
import re
import glob

# Ask for user input
user_input = input("Enter the string in common between CSV and HTML: ")

# Importing the HTML file
current_directory = os.getcwd()
html_files = glob.glob(os.path.join(current_directory, '*.html'))
matching_html = [file for file in html_files if user_input.lower() in file.lower()]
squad = pd.read_html(matching_html[0], encoding="UTF-8", thousands=".", decimal=",")[0]

# Importing the CSV file
current_directory = os.getcwd()
csv_files = glob.glob(os.path.join(current_directory, '*.csv'))
matching_csv = [file for file in csv_files if user_input.lower() in file.lower()]
genie_data = pd.read_csv(matching_csv[0], encoding="latin1", sep=';')

# Replacing values
squad.fillna(0, inplace=True)
squad.replace("-", 0, inplace=True)

# Fixing Average Rating
squad["Av Rat"] = squad["Av Rat"].astype(int) / 100
squad["Av Rat"].replace(0, "-", inplace=True)

# Fixing Starts and Subs columns
squad['Subs'] = squad['Apps'].str.extract(r'\((\d+)\)').fillna(0).astype(int)
squad['Starts'] = squad['Starts'].astype(int)
squad['Apps'] = squad['Starts'] + squad['Subs']
squad.drop(columns=['Starts'], inplace=True)

# Fixing Contract date
squad['Expires'] = pd.to_datetime(squad['Expires'], format='%d/%m/%Y')

# Fixing Height and Weight values
squad['Height'] = squad['Height'].astype(str).str.replace(' cm', '').astype(int)
squad['Weight'] = squad['Weight'].astype(str).str.replace(' kg', '').astype(int)

# Turning Wage column into numeric value
squad['Wage_Aux'] = squad['Wage'].str.replace('.', '', regex=True).str[2:-4]
squad['Wage'] = squad['Wage_Aux'].fillna(0).astype(int)

# Turning Value column into numeric value and deleting Aux columns
if not (squad['AP'] == 0).all():
    squad['Aux1'] = squad['AP'].str[-1]
    possible_values_aux = [(squad['Aux1'] == '0'), (squad['Aux1'] == 'K'), (squad['Aux1'] == 'M')]
    replacements_aux = [0, 1000, 1000000]
    squad['Aux2'] = np.select(possible_values_aux, replacements_aux, default=0)
    squad['Aux3'] = squad['AP'].str[2:]
    squad['Aux4'] = squad['Aux3'].apply(lambda x: 0 if x == '0' else x[:-1])
    squad['Aux4'] = squad['Aux4'].str.replace(',', '.').fillna(0).astype(float)
    squad['AP'] = squad['Aux4'] * squad['Aux2']
    squad['AP'] = squad['AP'].astype(int)
    squad.drop(columns=['Aux1', 'Aux2', 'Aux3', 'Aux4'], inplace=True)

squad.replace("-", 0, inplace=True)

# Remove percentage sign
for column in ['Pas %', 'Cr C/A', 'Tck R']:
    squad[column] = squad[column].str.replace('%', '')

squad.fillna(0, inplace=True)

# Transform to int
columns_to_int = [
    'Apps', 'Gls', 'Ast', 'PoM', 'Mins', 'WR.1', 'Det', 'Amb', 'Prof', 'Inj Pr',
    'Height', 'Weight', 'Tea', 'Wor', 'Ant', 'Cnt', 'Dec', 'AP', 'Drb', 'ShT',
    'Shots', 'Pens', 'Pens S', 'K Pas', 'OP-KP', 'CCC', 'Pas A', 'Ps C', 'Cr A',
    'Cr C', 'K Tck', 'Tck W', 'Itc', 'Blk', 'Hdrs',
    'Subs', 'Pas %', 'Cr C/A', 'Tck R'
]

squad[columns_to_int] = squad[columns_to_int].astype(int)
    
# Transform to float
columns_to_float = ['Av Rat', 'xG', 'Gls/90', 'NP-xG', 'xA', 'Poss Won/90', 'xGP', 'Clear']
squad[columns_to_float] = squad[columns_to_float].astype(float)

# Creating DNA column
squad['DNA'] = round(squad[['Det', 'Tea', 'Wor', 'Ant', 'Cnt', 'Dec']].mean(axis=1), 0)

# Starting Genie scout transformation
genie = genie_data

# Renaming and removing columns
genie_renames = {
    'Unique ID': 'UID',
    'GK Rating': 'GK',
    'DR Rating': 'RB',
    'DC Rating': 'CB',
    'DL Rating': 'LB',
    'DM Rating': 'DM',
    'MC Rating': 'CM',
    'AMR Rating': 'RW',
    'AMC Rating': 'AM',
    'AML Rating': 'LW',
    'FS Rating': 'ST',
    'TS Rating': 'ST2',
    'GK Pot Rating': 'pGK',
    'DR Pot Rating': 'pRB',
    'DC Pot Rating': 'pCB',
    'DL Pot Rating': 'pLB',
    'DM Pot Rating': 'pDM',
    'MC Pot Rating': 'pCM',
    'AMR Pot Rating': 'pRW',
    'AMC Pot Rating': 'pAM',
    'AML Pot Rating': 'pLW',
    'FS Pot Rating': 'pST',
    'TS Pot Rating': 'pST2',}
genie.rename(columns=genie_renames, inplace=True)
genie_remove = ['Best Rating', 'PoD']
genie = genie.drop(columns=genie_remove)

# Remove percentage signs (%) from the rating columns
genie_positions = [
    'GK', 'RB', 'CB', 'LB', 'DM', 'CM', 'RW', 'AM', 'LW', 'ST', 'ST2']

genie_positions_pot = [
    'pGK', 'pRB', 'pCB', 'pLB', 'pDM', 'pCM', 'pRW', 'pAM', 'pLW', 'pST', 'pST2']

for column in genie_positions:
    genie[column] = genie[column].str.replace(',', '.')
    genie[column] = genie[column].str.replace('%', '')
    genie[column] = genie[column].astype(float)

for column in genie_positions_pot:
    genie[column] = genie[column].str.replace(',', '.')
    genie[column] = genie[column].str.replace('%', '')
    genie[column] = genie[column].astype(float)

# Getting the highest value between TS and FS and removing the other
genie['ST'] = genie[['ST', 'ST2']].max(axis=1)
genie['pST'] = genie[['pST', 'pST2']].max(axis=1)
genie.drop(columns=['ST2'], inplace=True)
genie.drop(columns=['pST2'], inplace=True)
genie_positions.remove('ST2')
genie_positions_pot.remove('pST2')

# Creating rating columns
genie['Rt1'] = genie[genie_positions].max(axis=1)
genie['Rt2'] = genie[genie_positions].apply(lambda row: sorted(row)[-2], axis=1)
genie['P1'] = genie[genie_positions].idxmax(axis=1)
genie['P2'] = genie[genie_positions].apply(lambda row: row.drop(row.idxmax()).idxmax(), axis=1)

# Creating potential columns
genie['Pt1'] = genie[genie_positions_pot].max(axis=1)
genie['Pt2'] = genie[genie_positions_pot].apply(lambda row: sorted(row)[-2], axis=1)
genie['PP1'] = genie[genie_positions_pot].idxmax(axis=1)
genie['PP2'] = genie[genie_positions_pot].apply(lambda row: row.drop(row.idxmax()).idxmax(), axis=1)

# Rounding the ratings
ratings_to_round = ['GK', 'RB', 'CB', 'LB', 'DM', 'CM', 'RW', 'AM', 'LW', 'ST', 'Rt1', 'Rt2']
potentials_to_round = ['pGK', 'pRB', 'pCB', 'pLB', 'pDM', 'pCM', 'pRW', 'pAM', 'pLW', 'pST', 'Pt1', 'Pt2']
genie[ratings_to_round] = genie[ratings_to_round].round(1)
genie[potentials_to_round] = genie[potentials_to_round].round(1)

# Selecting columns
genie_filter = genie[['UID', 'Rt1', 'Pt1']]

# Merging both
merge = pd.merge(squad, genie_filter, on='UID', how='inner')

order = [
    'Squad', 'UID', 'Position', '2nd Nat', 'Nat', 'Age', 'Name', 'Club', 'Rt1', 'DNA', 'Pt1',
    'Apps', 'Subs', 'Av Rat', 'Gls', 'Ast', 'PoM', 'Mins', 'Personality', 'WR.1', 'Det', 'Amb', 'Prof', 'Inj Pr', 'Height',
    'Weight', 'Tea', 'Wor', 'Ant', 'Cnt', 'Dec', 'AP', 'Wage', 'Expires', 'Opt Ext by Club', 'Media Description',
    'xG', 'Gls/90', 'NP-xG', 'Drb', 'ShT', 'Shots', 'Pens', 'Pens S', 'xA', 'K Pas', 'OP-KP', 'CCC',
    'Pas A', 'Ps C', 'Pas %', 'Cr A', 'Cr C', 'Cr C/A', 'Poss Won/90', 'K Tck', 'Tck W', 'Tck R', 'xGP', 'Itc',
    'Blk', 'Clear', 'Hdrs'
]

merge = merge[order]

merge['Pas %'] = merge['Pas %'] / 100
merge['Cr C/A'] = merge['Cr C/A'] / 100
merge['Tck R'] = merge['Tck R'] / 100

merge[['Av Rat', '2nd Nat', 'Pas %', 'Cr C/A', 'Tck R']] = merge[['Av Rat', '2nd Nat', 'Pas %', 'Cr C/A', 'Tck R']].replace(0, np.nan)

#merge.to_csv('Data_FM.csv', index=False, encoding='utf-8-sig', sep=';', decimal=',')

new_genie_order= [
    'UID', 'EU Member', 'Nation', 'Position', 'Age', 'Name', 'Rt1', 'Pt1', 'Club',
    'GK', 'RB', 'CB', 'LB', 'DM', 'CM', 'RW', 'AM', 'LW', 'ST'
]

genie = genie[new_genie_order]

with pd.ExcelWriter(f"Data {user_input}.xlsx", engine='xlsxwriter') as writer:
    # Write 'merge' DataFrame to the 'FM' sheet
    merge.to_excel(writer, sheet_name='FM', index=False)

    # Write 'genie' DataFrame to the 'Genie' sheet
    genie.to_excel(writer, sheet_name='Genie', index=False)

# Save the Excel file
writer.save()