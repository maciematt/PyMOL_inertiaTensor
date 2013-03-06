PyMOL_inertiaTensor
===================


http://www.pymolwiki.org/index.php/inertia_tensor


DESCRIPTION
    
    This script will draw the inertia tensor of the selection.

ARGUMENTS
    
    selection = string: selection for the atoms included in the tensor calculation

    name = string: name of the tensor object to be created {default: "tensor"}
    
    state = int: state/model in the molecule object used in the tensor calculation

    scaling = int {0, 1, or 2}: 0 for no scaling of the inertia axes, 1 for scaling
    according to molecular shape, 2 for scaling according to eigenvalues 
    {default: 0}

EXAMPLE
    
    PyMOL> run inertia_tensor.py
    PyMOL> tensor molecule_object & i. 2-58+63-120 & n. n+ca+c, "tensor_model5_dom2", 5, 1
    
NOTES
    
    Requires numpy.
