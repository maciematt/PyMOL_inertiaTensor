PyMOL_inertiaTensor
===================

This script will draw the eigenvectors of the inertia tensor of a selection. It should be placed in the same folder as the .pdb for which the tensor is to be produced. In this folder run PyMOL and load the script by issuing "run inertiaTensor.py". Then it can be used within PyMOL via the tensor command, e.g.:

cmd.tensor(molecule_object, name="tensor", resids="24-65+78-122", atoms="n+ca+c")

Requires: PyMOL, numpy.
