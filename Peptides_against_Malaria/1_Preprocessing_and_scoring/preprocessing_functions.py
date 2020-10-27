'''
author : Anantha S Rao

date : 18 Oct, 2020

organisation : iGEM IISER Pune

'''
import os
import subprocess
import time
import pandas as pd
#from chimera import runCommand as rc   

# The above line can be uncommented when running sturated_mutagenesis() on UCSF Chimera

def saturated_mutagenesis(model_no,chain_name,start_residue,stop_residue,input_path,file_name,output_path):

    """
    Perform saturated Mutagenesis (SM) of a given length of peptide submitted in .pdb format and return all mutants each in different files

    Args: 
        model_no (str) : The model number of the peptide of interest in the .pdb file
        
        chain_no (str) : Name of the Chain where SM is to be performed. Ex : 'A' , 'B' or ' ' 
        
        start_residue (int) : Residue number on the given chain and model where SM needs to be performed (started) 
        
        stop_residue (int) : Residue number on the given chain where the SM needs to be stopped. 
        
        input_path (str) : Path to the directory .pdb containing the peptide that needs to undergo SM
        
        file_name (str) : Name of the .pdb file submitted 
        
        output_path (str) : Name of the output directory where the new models are saved.

    Returns : 
        This script is to be run in UCSF Chimera and all models/mutants are returned in .pdb format in the output_directory 


    Raises : 
        UCSF Chimera only works with Python 2.x 

    Notes : 
        Visit Github.com/Anantha-Rao12/Peptides-against-Malaria for more info

    """

	aa_data = 'ala arg asn asp cys glu gln gly his ile leu lys met phe pro ser thr trp tyr val'.split()
	
	for residue_no in range(start_residue,stop_residue+1):
		for amino_acid in aa_data:
			rc("open "+ os.path.join(input_path,file_name))
			rc("swapaa "+str(amino_acid)+" #"+str(model_no)+":"+str(residue_no)+"."+chain_name)
			os.chdir(output_path)
			rc("write #"+str(model_no)+" Inh_1_"+str(residue_no)+"_"+str(amino_acid)+".pdb")
			rc("close all")
			os.chdir(input_path)
			


def AnalyseComplex(foldx_path, file_full_path):

    """
    Use the subprocess module to execute the --analyseComplexChains=A,B command of FoldX and obtain the Interaction Energy between two chains in a .pdb file

    Args:
        foldx_path (str) : local full/relative path of the FOLDX executable 

        file_path (str) : local full path to the .pdb file that is to be analysed 


    Returns : 
        Prints the time taken to  analyse, process and write the output a single .pdb file
        Output is the stdout from the terminal 

    Notes : 
        More information can be found here : foldxsuite.crg.eu/command/AnalyseComplex


    """
	
	data=[]
	start = time.time()
	process = subprocess.Popen(f'{foldx_path} --command=AnalyseComplex --pdb={file_full_path} --analyseComplexChains=A,B', shell=True, stdout=subprocess.PIPE)
	result = process.communicate()[0] 
	data.append(result)
	end=time.time()
	time_taken = end-start
	print(time_taken)
	return data
	

def make_df_combine(files_path1,files_path2,output_path,csv_file_name):
	
	""" Visit files_in path1 and files_in path2 to collect all foldx Summary.fxout files that was created by AnalyseComplex command.
	With os.listdir each file name is stored in lists called 'foldx_summary_files' via list comprehension. We then open each .fxout Summary file with 
	a context manager and store the last line of the file which has the required interaction data (tab separated). A list of lists is thus created 
	and finally grafted into a dataframe with Pandas that is written as a .csv file to the given 'output_path' with 'csv_file_name'."""
	
	listoflists =[]
	paths= [files_path1,files_path2]
	for path in paths:
		foldx_summary_files = [file for file in os.listdir(path) if file.startswith('Summary')]
		for file in os.listdir(foldx_summary_files):
			with open(os.path.join(path,file),'r') as rf:
				lines = rf.read().splitlines()
				data = lines[-1].split('\t')  #Obtain the last line in the Summary.fxout file
				header = lines[-2].split('\t') #Obtain the 2nd last line as header in the Summary.fxout file
				listoflists.append(data)
	df = pd.DataFrame(listoflists,columns=header)
	os.chdir(output_path)
	df.to_csv(os.path.join(output_path,csv_file_name))

