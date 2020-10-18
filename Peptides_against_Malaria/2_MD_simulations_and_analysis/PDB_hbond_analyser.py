import numpy as np
import os
import sys
import subprocess
import pandas as pd

def pdbnames(filename):
    with open(filename,'r') as rf:
        pdbnames = rf.read().splitlines()
    return pdbnames

def get_filename_from_file(fname):
    cmd = f"cat {fname} | grep '#'" 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    filename = ps.communicate()[0]
    filename = str(filename,'utf-8').split()
    return filename

def get_number_hbonds(fname):
    cmd = f"cat {fname} | tail -1" 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    hbonds = ps.communicate()[0]
    n_hbonds = str(hbonds,'utf-8')[0]
    return n_hbonds 

def get_hbonds_data(fname):
    cmd = f"cat {fname} | grep '^:' " 
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    hbonds = ps.communicate()[0]
    hbonds = str(hbonds,'utf-8')
    return hbonds

def get_dataframe_hbonds(fname):
    hbonds=get_hbonds_data(fname)
    hbonds_list = hbonds.split('\n')[:-1]
    clean_hbond_data = [i.split() for i in hbonds_list]
    return clean_hbond_data

def make_dataframe(listoflists,cols):
    df = pd.DataFrame(listoflists,columns=cols) 
    return df

def processing_pdbs(pdbnames):
    e_list= []
    for fname in pdbnames:
        print(f"Processing file : {fname}")
        n_hbonds = get_number_hbonds(fname)
        print(f"Found {n_hbonds} Hydrogen bonds in {fname}")
        data = get_dataframe_hbonds(fname)
        data = [[fname]+i for i in data]
        data = [i+[n_hbonds] for i in data]
        e_list = e_list + data
    return e_list

def main():

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
