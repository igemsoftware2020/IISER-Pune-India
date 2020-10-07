# iGEM-IISER-Pune-India

## Project Description

The WHO estimated that 228 million people contracted Malaria globally and 405,000 people died from it in 2018. Our project aims to develop a library of inhibitory peptide drugs against certain essential human-parasite protein interactions that cause malaria amidst growing resistance to current antimalarial therapeutics. We intend to use cyclotides (a type of stable plant proteins) as stable protein scaffolds for the delivery of these peptides. Using in-silico modelling and simulations, our dry lab team has designed short peptides that will potentially inhibit the protein interactions crucial for the invasion and survival of malaria parasites inside a human host. Our wet lab team has designed various experiments to clone and express the interacting host and parasite proteins, characterize the drug and reduce the toxicity of the grafted cyclotides. To address issues related to poor diagnostics, we have developed a diagnostic tool using convolutional neural networks and advanced deep learning algorithms to identify patients with malaria based on images of their blood smears.

All scripts, programs and description of software used for Protein Data Bank file processing, analysis, and Molecular Dynamics simulation can be found on this repository. 

## Inhibitor peptide design

We designed peptide inhibitors against essential falciparum membrane proteins and Human endothelial cell surface receptors using a Structural Biology and Bioinformatics approach. More information on the workflow can be found on our wiki page ([here](https://2020.igem.org/Team:IISER-Pune-India/Overview)). In brief, thw worflow involved : 
1. Literature Search and Mining the PDB database 
  We wrote a program that statically mines the PDB database and returns all the required information in the form of a compact .csv file (or as preferred by the user). Although better commercial softwares are available, our web-parser is efficient and easy to handle with. We have also written a tutorial that on how we did it and believe that this wil greatly help future teams deal with the data deluge in biology and in particularly the RCSB Database. 
  
2. PDB file preprocessing and scoring
  Details on preprocessing can be found on the modelling section of our wiki. Here we present the scipts we used to perform preprocessing, scoring of peptide inhibitors and data analysis. We have written our Python notebooks in a format that is easily readable to new teams and amatuers to help with get started with similar projects.  
  
3. Molecular Dynamics Simulations
  We performed three full-atom 100ns Molecular dynamics simulations for each inhibitor model using GROMACS 3.6 on the Parambrahma Supercomputer. Our objective was to understand the behaviour of the inhibitor over time, and determine the specific regions or atoms of the motif that are responsible for the binding. 


## DeleMa Detect

DeleMa Detect is our Artificial Intelligence based end-to-end Deep Learning software for the diagnosis of Malaria through blood smear images. Our envisioned model consists of a Foldscope, an easy-to-assemble and very cheap optical microscope, a paper centrifuge that will help in creating the blood smear and a Deep Learning model that is able to classify blood smear images taken from any phone as infected or not. Our computational team has developed the deep learning software with an accuracy of 97%. We plan to reduce the size of the app, without compromising on accuracy, so that it could be used on all kinds of mobile phones and in regions with poor internet connectivity as well.




<br><br>
<br><br>
For clarifications and queries -- [iGEM-IISER-Pune](mailto:igem@sac.iiserpune.ac.in?subject=[igem20_github])@2020
