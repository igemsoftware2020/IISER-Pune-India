import re
import numpy as np
import sys
import pandas as pd

def get_centroid(pdb_file, chain_name):

    """
    Obtain the co-ordinates of the centroid of a given chain of a set of molecules in .pdb format

    Args : 
        pdb_file (str) : Full/relative path to the .pdb file 

        chain_name (str) : Name of the chain whose Centroid co-ordinates are to be computed

    Returns : 
        A 3x1 array that are the x,y,z co-ordinates of the centroid (G)     

    """
	
    regexp = r'(ATOM\s+)(\S+)(\s+\S+\s*\w{3,4}\s)('+str(chain_name)+')(\s+\S+\s+)(-|\d)(\d{0,3}.\d{1,3})(\s+)(-|\d)(\d{0,3}.\d{1,3})(\s+)(-|\d)(\d{0,3}.\d{1,3})(\s+\S+\s+\S+\s+)([A-Z])'
            
    pattern = re.compile(regexp)

    atomic_wt_dict = { 'H' : 1, 'C' : 12, 'N'  : 14, 'O' : 16 , 'S' : 32}
            
    with open(pdb_file,'r') as rf:
        contents = rf.read()
        matches = pattern.finditer(contents)
            
    '''	
    Atom no -->  match.group(2)
    Chain name --> match.group(4)
    X co-ordinates --> match.group(6)+match.group(7)
    Y co-ordinates --> match.group(9)+match.group(10)
    Z co-ordinates --> match.group(12)+match.group(13)
    Atom -->  match.group(15)
    Atomic weight --> atomic_wt[match.group(15)]
    '''
            
    posn_array = np.zeros((3,1))
    wt = np.zeros((1,1))

    for match in matches:
        x_cord = float(match.group(6)+match.group(7))
        y_cord = float(match.group(9)+match.group(10))
        z_cord = float(match.group(12)+match.group(13))
        atomic_wt = atomic_wt_dict[match.group(15)]
        posn_array= np.hstack((posn_array,np.array([[x_cord],[y_cord],[z_cord]])))
        wt = np.hstack((wt,np.array([[atomic_wt]])))

    weighted_posn = posn_array * wt
    wt_sum = np.sum(wt,axis=1,keepdims=True)

    centroid = np.sum((weighted_posn/wt_sum),axis=1,keepdims=True)
    
    return centroid
    
    
def euclidean_distance(centroid1, centroid2):
    """
    Compute the Euclidean_distance between two Centroids 

    Args : 
        centroid1 : (3x1 numpy array ) 
        centroid2 :  (3x1 numpy array ) 

    Retuns :
        A Real number (float) that is the Euclidean distance between two 3D vectors 

    """
	
	distance_vector = centroid1-centroid2
	distance = np.sqrt(np.sum(distance_vector**2))
	
	return distance


def pdb_names2list(pdb_files_textfile):

    """
    Convert a file that contains names in each line into an element of a list 

    Args:
        pdb_files_testfile (str) : Full / relative path to the text file 

    Returns:
        A List where the i^(th) element is the i^(th) line in the test file
    """
    
    with open(pdb_files_textfile,'r') as rf:
        pdb_files = rf.read().split('\n')
        pdb_files = [item for item in pdb_files if item.endswith('.pdb')] 
        
    return pdb_files


def pdb_list_centroid2df(pdb_files, output_file):

    """
    Compute the distance between two Chains for all pdb files and return a .csv file 

    Args : 
        pdb_files (str) : Path to the text file containing all .pdb files

        output_fie (str) : Name of the putput .csv file that is saved in the same directory as this script 

    Returns : 
        A .csv file where each row represents a .pdb file with 4 Columns : ('Name','Centroid of Chain A','Centroid of Chain B','Euclidean Distance')


    """
    listoflists = []
    for f in pdb_files:
        try :
        
            cA = get_centroid(f,'A')
            cB = get_centroid(f,'B')
            distance = euclidean_distance(cA,cB)
            data = [f,cA,cB,distance]
            listoflists.append(data)
            print(f'The distance between the two centroids in {f} is {distance:.5} A ')
            
        except:
            print("PDB file error. Please check if all columns of PDB files are filled")

        df = pd.DataFrame(listoflists,columns =['Filename','CentroidA','CentroidB','Distance'])
        df.to_csv('./'+str(output_file)+'.csv',index=False)


def main():

    """ 
    Main wrapper function
    """

    print(' Processing \n')
    pdbfiles = pdb_names2list(sys.argv[1])
    pdb_list_centroid2df(pdbfiles , sys.argv[2])
    sys.stdout.write(f'\nProcess Successful! Output saved to {sys.argv[2]}.csv\n ')


if __name__ == '__main__':

    if len(sys.argv) !=  3 :
        print('\nERROR')
        print('Incorrect number of arguments submitted, expecting only 2.')
        print('1.Text file containing pdb file names and 2.output .csv filename')
        sys.exit(1)
    else:
        main()
        
        
