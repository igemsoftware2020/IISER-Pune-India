from modeller import *

env = environ()
aln = alignment(env)
mdl = model(env, file='model', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='model', atom_files='model.pdb')
aln.append(file='temp.ali', align_codes='temp')
aln.align2d()
aln.write(file='alignment.ali', alignment_format='PIR')
aln.write(file='alignment.pap', alignment_format='PAP')
