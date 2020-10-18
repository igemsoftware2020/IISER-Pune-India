# -*- coding: utf-8 -*-
"""5MZA-data-cleaning-analysis.ipynb

author : Anantha S Rao

date : Oct 18 2020

organization : IISER Puen India

Google Colab link : https://colab.research.google.com/drive/1-voXdwHeQ8rp5lLP5TePj1fhI7qio4Ms
"""

### CLEANING THE DATA .CSV file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path = './5mza-mastersheet.csv'
df = pd.read_excel(path, index_col=0)
df.head()

inhibitor_type = 'i 1 2 3 4 5'.split()
inh_len = [np.nan,9,8,10,6,6]
inh_data = dict(zip(inhibitor_type,inh_len))

df['fname'] = df['Pdb'].str.split('/').apply(lambda x : x[-1])
df.drop('Pdb',axis=1,inplace=True)

df['inhibitor_type'] = df.fname.str.split('_').apply(lambda x : x[0]).apply(lambda x : x[3])

df['Group2_len'] = df['inhibitor_type'].replace(inh_data)

df['inhibitor_type'].replace({'i':'wild_type'},inplace=True)

df['mresidue_no'] = df.fname.str.split('_').apply(lambda x : x[1] if len(x)>1 else np.NAN)  # mutated residue number

df['swapaa'] = df.fname.str.split('_').apply(lambda x : x[-1]).apply(lambda x : x[:-4])
df['swapaa'].replace('(inhibitor\w)',np.NAN,regex=True,inplace=True)

wtype_group2_len = [9,8,10,6,6]
df.loc[df.fname.str.match(r'(^inhib)')==True,'Group2_len'] = wtype_group2_len

cols = df.columns.tolist()
cols = cols[-5:] + cols[0:7]
df_new = df[cols]

# write dataframe to external file
df_new.to_csv('./5MZA-cleaned-csv')



### ANALYSING THE CLEANED DATA .CSV file


path = './5MZA-cleaned-csv'

df = pd.read_csv(path)
df.drop('Unnamed: 0',axis=1,inplace=True)


wild_type = df[df.inhibitor_type=='wild_type']
wild_type

wild_type['Interaction Energy'].plot.bar(alpha=0.3)

wild_type['StabilityGroup2'].plot.bar()

sns.barplot(x='fname',y='Interaction Energy', data=wild_type)



df1 = df[['fname', 'inhibitor_type', 'Group2_len', 'mresidue_no', 'swapaa','IntraclashesGroup2',
       'Interaction Energy', 'StabilityGroup2']].sort_values('Interaction Energy',ascending=True)
       
df_wt = df1[df1.inhibitor_type=='wild_type'] #contains DataFrame with wild-type data
df_mut = df1[df1.inhibitor_type !='wild_type']  #contains mutant data




def  print_hybrid_peptide(df,best_model_no) : 

	best_model = df_mut[df_mut['inhibitor_type']== 'best_model_no']

	best_model_energy_min = best_model.loc[best_model.groupby("mresidue_no")["Interaction Energy"].idxmin()]
	
	return best_model_energy_min

# Relationship between inhibitor type and Interaction energy


def plot_swarmplot(df): 

	fig,axes = plt.subplots(nrows=2,ncols=1,figsize=(15,13))

	sns.despine()
	sns.axes_style("whitegrid")
	sns.set_context("talk")

	sns.swarmplot(x='inhibitor_type',y='Interaction Energy',hue='swapaa',data=df_mut, ax=axes[0], palette='gnuplot',dodge=True)
	sns.barplot(x='fname',y='Interaction Energy',data=wild_type, ax=axes[0],alpha=0.29,palette='dark', label='wild-type')

	sns.swarmplot(x='inhibitor_type',y='StabilityGroup2',hue='swapaa',data=df_mut, ax=axes[1], palette='gnuplot',dodge=True)
	sns.barplot(x='fname',y='StabilityGroup2',data=wild_type, ax=axes[1],palette='dark',alpha=0.29)

	axes[0].set_xlabel('', fontsize=18)
	axes[0].set_ylabel('Interaction Energy', fontsize=22)
	axes[1].set_xlabel('Inhibitor Type', fontsize=22)
	axes[1].set_ylabel('Stability of Peptide', fontsize=22)

	
	axes[0].legend(bbox_to_anchor=(1.05, 1), loc=2,fancybox=True, framealpha=1, shadow=True, borderpad=1)
	axes[1].legend_.remove()

	axes[0].tick_params(axis='both', which='major', labelsize=10)

	axes[0].set_xticklabels(['model1 (len=9)','model2 (len=8)','model3 (len=10)','model4 (len=6)','model5 (len=6)'])
	axes[1].set_xticklabels(['model1 (len=9)','model2 (len=8)','model3 (len=10)','model4 (len=6)','model5 (len=6)'])

	axes[0].tick_params(labelsize=14)
	axes[1].tick_params(labelsize=14)

	plt.suptitle('5MZA Computational Saturated Mutagenesis Results', fontsize=26)
	
	return fig,axes


### Aliter to obtain swarmplot 


def plot_second_swarmplot(df):

	fig,axes = plt.subplots(nrows=5,ncols=1,figsize=(16,17))

	sns.set_style("whitegrid")
	sns.despine()
	for i in range(5):
	    sns.swarmplot(x='mresidue_no',y='Interaction Energy', data = df_mut[df_mut['inhibitor_type']== str(i+1)], palette='gnuplot',alpha=0.8, ax=axes[i], hue='swapaa',dodge=True)
	    val = wild_type['Interaction Energy'][wild_type.fname=='inhibitor'+str(i+1)+'.pdb'].values[0]
	    axes[i].axhline(val,ls='--',color='black', label='wild-type',alpha=0.5)
	    axes[i].set_xlabel('Residue number',fontsize=18)
	    if i!=0:
		  axes[i].legend_.remove()
	    else:
		  axes[i].legend(bbox_to_anchor=(1.2, -0.2),fancybox=True, framealpha=1, shadow=True, borderpad=1)
		  axes[i].legend_.set_title('Model'+str(i+1))

	plt.suptitle('5MZA Computational Saturated Mutagenesis results')
	
	return fig,axes


def def plot_third_swarmplot(df):

	fig,axes = plt.subplots(nrows=5,ncols=1,figsize=(12,16))

	sns.set_style("whitegrid")
	sns.despine()
	sns.swarmplot(x='mresidue_no',y='Interaction Energy', data = df_mut[df_mut['inhibitor_type']== '1'], palette='gnuplot',alpha=0.8, ax=axes[0])
	sns.swarmplot(x='mresidue_no',y='Interaction Energy', data = df_mut[df_mut['inhibitor_type']== '2'], palette='gnuplot',alpha=0.8, ax=axes[1])
	sns.swarmplot(x='mresidue_no',y='Interaction Energy', data = df_mut[df_mut['inhibitor_type']== '3'], palette='gnuplot',alpha=0.8, ax=axes[2])
	sns.swarmplot(x='mresidue_no',y='Interaction Energy', data = df_mut[df_mut['inhibitor_type']== '4'], palette='gnuplot',alpha=0.8, ax=axes[3])
	sns.swarmplot(x='mresidue_no',y='Interaction Energy', data = df_mut[df_mut['inhibitor_type']== '5'], palette='gnuplot',alpha=0.8, ax=axes[4])

	for i in range(5):
	    axes[i].legend(bbox_to_anchor=(1.05, 1), loc=5,fancybox=True, framealpha=1, shadow=True, borderpad=1)
	    axes[i].legend_.set_title('Model'+str(i+1))
	    axes[i].set_xlabel('Residue number')
	    axes[i].set_ylabel('Interaction Energy',fontsize=16)_t

	plt.suptitle('5MZA Saturated Mutagenesis results')
	plt.tight_layout()
	
	return fig,axes
plt.show()

