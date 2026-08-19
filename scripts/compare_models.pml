reinitialize

load structures/alphafold-P35372.pdb, alphafold
load structures/swissmodel-P35372.pdb, swissmodel

hide everything
show cartoon, alphafold or swissmodel
color marine, alphafold
color limegreen, swissmodel

align alphafold and name CA, swissmodel and name CA
set cartoon_transparency, 0.15, alphafold
set ray_opaque_background, off
bg_color white
orient alphafold or swissmodel
zoom alphafold or swissmodel
