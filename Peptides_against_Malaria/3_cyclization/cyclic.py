from modeller import *
from modeller.automodel import *

log.verbose()
env = environ()

# Disable default NTER and CTER patching
env.patch_default = False 

class MyModel(automodel):
    def special_patches(self, aln):
        # Link between last residue (-1) and first (0) to make chain cyclic:
        self.patch(residue_type='LINK',
                   residues=(self.residues[-1], self.residues[0]))

# Use the new 'MyModel' class rather than 'automodel'
a = MyModel(env, alnfile='alignment.ali', knowns='model', sequence='temp')

a.starting_model = a.ending_model = 1
a.make()

