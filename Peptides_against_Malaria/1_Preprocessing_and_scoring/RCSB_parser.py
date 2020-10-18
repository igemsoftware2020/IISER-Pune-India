
Skip to content
Pull requests
Issues
Marketplace
Explore
@Anantha-Rao12
Learn Git and GitHub without any code!

Using the Hello World guide, you’ll start a branch, write comments, and open a pull request.
Anantha-Rao12 /
Peptides-against-Cerebral-Malaria

1
0

    2

Code
Issues
Pull requests
Actions
Projects
Wiki
Security 1
Insights

    Settings

Peptides-against-Cerebral-Malaria/Preprocessing-data/PDB-web-parser.py /
@Anantha-Rao12
Anantha-Rao12 updated web-parser
Latest commit 28524c8 on Aug 15
History
1 contributor
We found potential security vulnerabilities in your dependencies.

Only the owner of this repository can see this message.
135 lines (106 sloc) 4.19 KB
Code navigation is available!

Navigate your code with ease. Click on function and method calls to jump to their definitions or references in the same repository. Learn more
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

path = 'D:\\IGEM\\Cyclotide-malaria\\Malarial-peptides\\pdb-ids.csv'   ### Path of csv file containing all pdb-ids downloaded from PDB-advanced-search-options
with open(path, 'r') as file:    ### reading the file with a context manager
    pdb_id = file.read().split(',')     ### create a list containing pdb-ids
    
    
m = len(pdb_id)   ### length of pdb_id list ie no of pdb_ids
    
   

PDB_ID, Desc, Classification, Exp_system, Method, Lit, Pubmed_id, Pubmed_abs, Org1, Mmol, Org2, Mut, Res = [
], [], [], [], [], [], [], [], [], [], [], [], []


for i in range(m, len(pdb_id)):
    url = 'https://www.rcsb.org/structure/'+pdb_id[i]

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    primary_data = soup.find('div', class_="col-md-8 col-sm-12 col-xs-12")
    secondary_data = soup.find('div', class_='tab-content')

    # COLLECTING DATA
    PDB_ID.append(pdb_id[i])

    try:
        desc = primary_data.h4.text
        Desc.append(desc)
    except:
        Desc.append(None)

    try:
        classification = primary_data.find('li', id='header_classification').a.text
        Classification.append(classification)
    except:
        Classification.append(None)

    try:
        exp_sys = primary_data.find('li', id="header_expression-system").a.text
        Exp_system.append(exp_sys)
    except:
        Exp_system.append(None)

    try:
        method = primary_data.find('li', id='exp_header_0_method').strong.next_sibling
        Method.append(method)
    except:
        Method.append(None)

    try:
        literature = primary_data.find('div', id='primarycitation').h4.text
        Lit.append(literature)
    except:
        Lit.append(None)

    try:
        pubmed_id = primary_data.find('li', id='pubmedLinks').a.text
        Pubmed_id.append(pubmed_id)
    except:
        Pubmed_id.append(None)

    try:
        pubmed_abstract = primary_data.find('div', class_='hidden-print').p.text
        Pubmed_abs.append(pubmed_abstract)
    except:
        Pubmed_abs.append(None)

    try:
        macromolecules = secondary_data.find_all('div', class_='table-responsive')
        macromolecules = [i.td.text for i in macromolecules]
        Mmol.append(macromolecules)
    except:
        Mmol.append(None)

    try:
        org1 = primary_data.find('li', id='header_organism').find_all('a')[0].text
        Org1.append(org1)
    except:
        Org1.append(None)

    try:
        org2 = primary_data.find('li', id='header_organism').find_all('a')[1].text
        Org2.append(org2)
    except:
        Org2.append(None)

    try:
        mutation = primary_data.find('li', id='header_mutation').strong.next_sibling.split('&')[0]
        Mut.append(mutation)
    except:
        Mut.append(None)

    try:
        if method == 'ELECTRON MICROSCOPY':
            resolution = primary_data.find(
                'li', id="exp_header_0_em_resolution").strong.next_sibling.split('&')[0]
            Res.append(resolution)

        elif method == 'X-RAY DIFFRACTION':
            resolution = primary_data.find(
                'li', id="exp_header_0_diffraction_resolution").strong.next_sibling
            Res.append(resolution)

        elif method == 'SOLUTION NMR':
            resolution = primary_data.find(
                'li', id="exp_header_0_nmr_selectionCriteria").strong.next_sibling.split('&')[0]
            Res.append(resolution)

    except:
        Res.append(None)


dataframe_dict = {'PDB_ID': PDB_ID,
             'Description': Desc,
             'Classification': Classification,
             'Expression-System': Exp_system,
             'Mutation': Mut,
             'Method': Method,
             'Resolution': Res,
             'Macromolecules': Mmol,
             'Organism1': Org1,
             'Organism2': Org2,
             'Literature': Lit,
             'Pubmed_id': Pubmed_id,
             'Pubmed_abstract': Pubmed_abs
             }

with open('D:\\IGEM\\Cyclotide-malaria\\Malarial-peptides\\null_data2.txt', 'w') as f:
    f.write(json.dumps(dataframe_dict))    ### Dump data as .json file

test_df = pd.DataFrame(dataframe_dict) ### Create a Dataframe from dictionary ; can we write to a csv or anyother preferred format
