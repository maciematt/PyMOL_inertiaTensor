PyMOL_inertiaTensor
===================

http://www.pymolwiki.org/index.php/inertia_tensor.py
(c) August 2010 by Mateusz Maciejewski
matt (at) mattmaciejewski . com

Licnese: MIT

DESCRIPTION

  This script will draw the eigenvectors of the inertia tensor of the selection.

ARGUMENTS

  selection = string: selection for the atoms included in the tensor calculation

  name = string: name of the tensor object to be created {default: "tensor"}

  state = int: state/model in the molecule object used in the tensor calculation

EXAMPLE

  PyMOL> run inertia_tensor.py
  PyMOL> tensor molecule_object & i. 2-58+63-120 & n. n+ca+c, "tensor_model5_dom2", 5

NOTES

  Requires numpy.
