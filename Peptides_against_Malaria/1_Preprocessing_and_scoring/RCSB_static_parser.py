
Skip to content
Pull requests
Issues
Marketplace
'''
author : Anantha S Rao

date : Oct 12, 2020

organization : iGEM IISER Pune

'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json



def read_pdb_ids_csv(csv_path):

	path = './pdb-ids.csv'   ### Path of csv file containing all pdb-ids downloaded from PDB-advanced-search-options
	with open(path, 'r') as file:    ### reading the file with a context manager
	    pdb_id_list = file.read().split(',')     ### create a list containing pdb-ids
	    
    return pdb_id_list   


def get_pdb_details(pdb_id):

    '''PDB_ID, Desc, Classification, Exp_system, Method, Lit, Pubmed_id, Pubmed_abs, Org1, Mmol, Org2, Mut, Res is the order of items needed'''

    pdb_details = []
    url = 'https://www.rcsb.org/structure/'+pdb_id

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    primary_data = soup.find('div', class_="col-md-8 col-sm-12 col-xs-12")
    secondary_data = soup.find('div', class_='tab-content')

    ### COLLECTING DATA FOR ONE PDB ID
    
    PDB_ID.append(pdb_id)

    try:
        desc = primary_data.h4.text
        pdb_details.append(desc)
    except:
        pdb_details.append(None)

    try:
        classification = primary_data.find('li', id='header_classification').a.text
        pdb_details.append(classification)
    except:
        pdb_details.append(None)

    try:
        exp_sys = primary_data.find('li', id="header_expression-system").a.text
        pdb_details.append(exp_sys)
    except:
        pdb_details.append(None)

    try:
        method = primary_data.find('li', id='exp_header_0_method').strong.next_sibling
        pdb_details.append(method)
    except:
        pdb_details.append(None)

    try:
        literature = primary_data.find('div', id='primarycitation').h4.text
        pdb_details.append(literature)
    except:
        pdb_details.append(None)

    try:
        pubmed_id = primary_data.find('li', id='pubmedLinks').a.text
        pdb_details.append(pubmed_id)
    except:
        pdb_details.append(None)

    try:
        pubmed_abstract = primary_data.find('div', class_='hidden-print').p.text
        pdb_details.append(pubmed_abstract)
    except:
        pdb_details.append(None)

    try:
        macromolecules = secondary_data.find_all('div', class_='table-responsive')
        macromolecules = [i.td.text for i in macromolecules]
        pdb_details.append(macromolecules)
    except:
        pdb_details.append(None)

    try:
        org1 = primary_data.find('li', id='header_organism').find_all('a')[0].text
        pdb_details.append(org1)
    except:
        pdb_details.append(None)

    try:
        org2 = primary_data.find('li', id='header_organism').find_all('a')[1].text
        pdb_details.append(org2)
    except:
        pdb_details.append(None)

    try:
        mutation = primary_data.find('li', id='header_mutation').strong.next_sibling.split('&')[0]
        pdb_details.append(mutation)
    except:
        pdb_details.append(None)

    try:
        if method == 'ELECTRON MICROSCOPY':
            resolution = primary_data.find(
                'li', id="exp_header_0_em_resolution").strong.next_sibling.split('&')[0]
            pdb_details.append(resolution)

        elif method == 'X-RAY DIFFRACTION':
            resolution = primary_data.find(
                'li', id="exp_header_0_diffraction_resolution").strong.next_sibling
            pdb_details.append(resolution)

        elif method == 'SOLUTION NMR':
            resolution = primary_data.find(
                'li', id="exp_header_0_nmr_selectionCriteria").strong.next_sibling.split('&')[0]
            pdb_details.append(resolution)

    except:
        pdb_details.append(None)

    return pdb_details # returns a list containing all required values


def main(csv_path, col_names):
    pdb_ids_list = read_pdb_ids_csv(csv_path)        
    m = len(pdb_id)   ### length of pdb_id list ie no of pdb_ids
    
    dataframe = []
    for i in range(m):
        dataframe.append(get_pdb_details(pdb_ids_list[i]))

    dataframe = pd.DataFrame(dataframe, columns=col_names)

    return dataframe

column_namaes = ['PDB_ID', ' Desc' , ' Classification', ' Exp_system' , ' Mut' , ' Method' , ' Res', ' Mmol', ' Org1',' Org2', ' Lit', ' Pubmed_id', ' Pubmed_abs']

dataframe = main(csv_path,column_namaes) 
dataframe.to_csv('./rscb_data_cleaned.csv')  ### write output to a csv file

### The object 'dataframe' can then be converted to other data types (json, pkl) and used for further analysis.
