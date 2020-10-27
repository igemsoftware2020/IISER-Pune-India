import numpy as np  # for array operations
import os
import sys
import subprocess    # used to pass UNIX CLI commands
import pandas as pd  # creating a dataframe and saving

def pdbnames(filename):
    with open(filename,'r') as rf:
        pdbnames = rf.read().splitlines()
    return pdbnames

def get_filename_from_file(fname): # obtaining the timestamp from the passed text.info file
    cmd = f"cat {fname} | grep '#'" 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    filename = ps.communicate()[0]
    filename = str(filename,'utf-8').split()
    return filename

def get_number_hbonds(fname): # gives the number of hbonds found at that timestamp / pdb file 
    cmd = f"cat {fname} | tail -1" 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    hbonds = ps.communicate()[0]
    n_hbonds = str(hbonds,'utf-8')[0]
    return n_hbonds 

def get_hbonds_data(fname):   # gives information on the Donor Acceptor pairs of Hyrogen bonds fund in that timestamp / PDB file
    cmd = f"cat {fname} | grep '^:' " 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    hbonds = ps.communicate()[0]
    hbonds = str(hbonds,'utf-8')
    return hbonds

def get_dataframe_hbonds(fname):    # returns a list of lists where each list contains hbond info and the number of elements correspond to the number of hbonds
    hbonds=get_hbonds_data(fname)
    hbonds_list = hbonds.split('\n')[:-1]
    clean_hbond_data = [i.split() for i in hbonds_list]
    return clean_hbond_data

def make_dataframe(listoflists,cols): # used to make the final dataframe
    df = pd.DataFrame(listoflists,columns=cols) 
    return df

def processing_pdbs(pdbnames):  # create a dataframe and loop through all specified files
    list_of_list= []
    for fname in pdbnames:
        print(f"Processing file : {fname}")
        n_hbonds = get_number_hbonds(fname)
        print(f"Found {n_hbonds} Hydrogen bonds in {fname}")
        data = get_dataframe_hbonds(fname)
        data = [[fname]+i for i in data]
        data = [i+[n_hbonds] for i in data]
        list_of_lists.append(data)
    return e_list

def main():
    """ 
    Main wrapper function 
    """

    hbond_info_files = pdbnames(sys.argv[1])
    data = processing_pdbs(hbond_info_files)
    df = make_dataframe(data,cols)

    return df

cols = ['Fname','Donor','Acceptor','Hydrogen','DA dist','D-H_A dist','n_hbonds']

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("\nERROR")
        print("Incorrect number of arguments submitted, expecting only 2")
        print("1. Text file containing _hbond_info.txt file names and output .csv filename")
        print("NOTE : All files and this executable must be in the same directory")
    else:
        df = main()
        df.to_csv(sys.argv[2]+'.csv')
        print(f"Wrote output to {sys.argv[2]}")
