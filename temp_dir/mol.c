#include "mol.h"

//Sets the values of an atom
void atomset(atom *atom, char element[3], double *x, double *y, double *z) {
    //Checking if the atom to set is NULL
    if(atom == NULL) {
        return;
    }
    
    //Setting the values in the atom
    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

//Gets the values of an atom (pass by reference)
void atomget(atom *atom, char element[3], double *x, double *y, double *z) {
    //Checking if the atom to set is NULL
    if(atom == NULL) {
        return;
    }
    
    //Getting the values from the atom
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

//Sets the values of a bond
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;

    compute_coords(bond);
}

//Gets the values of a bond (pass by reference)
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}

//Calculates and sets the numerical values of a bond
void compute_coords( bond *bond ) {
    atom atomOne = bond->atoms[bond->a1];
    atom atomTwo = bond->atoms[bond->a2];

    bond->x1 = atomOne.x;
    bond->x2 = atomTwo.x;
    bond->y1 = atomOne.y;
    bond->y2 = atomTwo.y;
    bond->z = (atomOne.z + atomTwo.z)/2;
    bond->len = sqrt(pow(( atomTwo.x - atomOne.x), 2) + pow((atomTwo.y - atomOne.y), 2));
    bond->dx = (atomTwo.x - atomOne.x)/bond->len;
    bond->dy = (atomTwo.y - atomOne.y)/bond->len;
}

//Allocates sufficient space for a molecule
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
    //Attempting to allocate space for the molecule
    molecule *newMol = malloc(sizeof(molecule));
    if(newMol == NULL) {
        return NULL;
    }

    //Assigning default atom,bond counter values
    newMol->atom_max = atom_max;
    newMol->atom_no = 0;
    newMol->bond_max = bond_max;
    newMol->bond_no = 0;

    //Attempting to allocate space for the atom component
    newMol->atoms = malloc(sizeof(atom) * atom_max);
    newMol->atom_ptrs = malloc(sizeof(atom*) * atom_max);
    if((newMol->atoms == NULL) || (newMol->atom_ptrs == NULL)) {
        molfree(newMol);
        return NULL;
    } 

    //Attempting to allocate space for the bond component
    newMol->bonds = malloc(sizeof(bond) * bond_max);
    newMol->bond_ptrs = malloc(sizeof(bond*) * bond_max);
    if((newMol->bonds == NULL) || (newMol->bond_ptrs == NULL)) {
        molfree(newMol);
        return NULL;
    }

    //Assigning bond/atom ptrs to corresponding bonds/atoms array
    for(int i = 0; i < atom_max; i++) {
        newMol->atom_ptrs[i] = &(newMol->atoms[i]);
    }

    for(int i = 0; i < bond_max; i++) {
        newMol->bond_ptrs[i] = &(newMol->bonds[i]);
    }

    return newMol;
}

//Copys the contents of the src molecule into a duplicate molecule
molecule *molcopy(molecule *src) {
    //Checking if a null molecule was passed
    if(src == NULL) {
        return NULL;
    }

    //Attempting to allocate space for a new molecule
    molecule *newMol = molmalloc(src->atom_max, src->bond_max);
    if(newMol == NULL) {
        return NULL;
    }

    //Appending all the atoms
    for(int i = 0; i < src->atom_no; i++) {
        molappend_atom(newMol, &(src->atoms[i]));
    }

    //Appending all the bonds
    for(int i = 0; i < src->bond_no; i++) {
        molappend_bond(newMol, &(src->bonds[i]));
        newMol->bonds[i].atoms = newMol->atoms;
    }

    return newMol;
}

//Freeing a molecule
void molfree(molecule *ptr) {
    if(ptr != NULL) {
        free(ptr->atoms);
        free(ptr->atom_ptrs);
        free(ptr->bonds);
        free(ptr->bond_ptrs);
        free(ptr);
    }
}

//Appends an atom into the next available spot in a molecule
void molappend_atom(molecule *molecule, atom *atom) {
    //Returning if the passed molecule is NULL since an atom cannot be appended
    if(molecule == NULL) {
        return;
    }

    //Incrementing atom_max if necessary
    if(molecule->atom_no == molecule->atom_max) {
        if(molecule->atom_max == 0) {
            molecule->atom_max = 1;
        } else {
            molecule->atom_max *= 2;
        }

        //Reallocating space for atoms and atom_ptrs
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom)*(molecule->atom_max));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*)*(molecule->atom_max));
        
        //Exiting the program if realloc fails
        if((molecule->atoms == NULL) || (molecule->atom_ptrs == NULL)) {
            molfree(molecule);
            exit(1);
        } else {
            //Reassigning atom ptrs for when realloc moves the atoms array
            for(int i = 0; i < molecule->atom_no; i++) {
                molecule->atom_ptrs[i] = &(molecule->atoms[i]);
            }
        }
    }

    //Updating atom information into the molecule
    molecule->atoms[molecule->atom_no] = *atom;
    molecule->atom_ptrs[molecule->atom_no] = &(molecule->atoms[molecule->atom_no]);
    molecule->atom_no += 1;
}

//Appends an bond into the next available spot in a molecule
void molappend_bond(molecule *molecule, bond *bond) {
    //Incrementing bond_max if necessary
    if(molecule->bond_no == molecule->bond_max) {
        if(molecule->bond_max == 0) {
            molecule->bond_max = 1;
        } else {
            molecule->bond_max *= 2;
        }

        //Reallocating space for bonds and bond_ptrs
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond)*(molecule->bond_max));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*)*(molecule->bond_max));
        
        //Exiting the program if realloc fails
        if((molecule->bonds== NULL) || (molecule->bond_ptrs == NULL)) {
            molfree(molecule);
            exit(1);
        } else {
            //Reassigning bond ptrs for when realloc moves the atoms array
            for(int i = 0; i < molecule->bond_no; i++) {
                molecule->bond_ptrs[i] = &(molecule->bonds[i]);
            }
        }
    }

    //Updating bond information into the molecule
    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &(molecule->bonds[molecule->bond_no]);
    molecule->bond_no += 1;
}

//Sorts the atom_ptrs and bond_ptrs array in a molecule
void molsort(molecule *molecule) {
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), atom_cmp);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_cmp);
}

//Atom compare function for qsort
int atom_cmp(const void *a, const void *b) {
    atom *a_ptr, *b_ptr;
    
    a_ptr = *(struct atom **)a;
    b_ptr = *(struct atom **)b;

    if(a_ptr->z > b_ptr->z) {
        return 1;
    } else if (a_ptr->z == b_ptr->z) {
        return 0;
    } else {
        return -1;
    }
}

//Bond compare function for qsort
int bond_cmp(const void *a, const void *b) {
    bond *a_ptr, *b_ptr;
    
    a_ptr = *(struct bond **)a;
    b_ptr = *(struct bond **)b;

    if(a_ptr->z > b_ptr->z) {
        return 1;
    } else if (a_ptr->z == b_ptr->z) { //Potentially change to fabs(a - b) < epsilon
        return 0;
    } else {
        return -1;
    }
}

//Converts a given degree to radians
double degToRad(unsigned short deg) {
    return deg * PI / 180;
}

//Sets the xform_matrix with an x rotation by deg degrees
void xrotation(xform_matrix xform_matrix, unsigned short deg) {
    double rad = degToRad(deg);

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = -sin(rad);

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

//Sets the xform_matrix with an y rotation by deg degrees
void yrotation(xform_matrix xform_matrix, unsigned short deg) {
    double rad = degToRad(deg);

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -sin(rad);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

//Sets the xform_matrix with an z rotation by deg degrees
void zrotation(xform_matrix xform_matrix, unsigned short deg) {
    double rad = degToRad(deg);

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = -sin(rad);
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

//Performs a rotation given by xform_matrix on each atom in the molecule
void mol_xform(molecule *molecule, xform_matrix matrix) {
    double newX, newY, newZ;

    for (int i = 0; i < molecule->atom_no; i++) {
        newX = molecule->atoms[i].x * matrix[0][0] + molecule->atoms[i].y * matrix[0][1] + molecule->atoms[i].z * matrix[0][2];
        newY = molecule->atoms[i].x * matrix[1][0] + molecule->atoms[i].y * matrix[1][1] + molecule->atoms[i].z * matrix[1][2];
        newZ = molecule->atoms[i].x * matrix[2][0] + molecule->atoms[i].y * matrix[2][1] + molecule->atoms[i].z * matrix[2][2];

        molecule->atoms[i].x = newX;
        molecule->atoms[i].y = newY;
        molecule->atoms[i].z = newZ;
    }

    for(int i = 0; i < molecule->bond_no; i++) {
        compute_coords(molecule->bond_ptrs[i]);
    }
}

//Create and setup a rotations structure
rotations *spin(molecule *mol) {
    //Checking if passed mol is valid
    if(mol == NULL) {
        return NULL;
    }

    //Attempting to allocate a rotation structure
    rotations *rotMols = malloc(sizeof(struct rotations));
    if(rotMols == NULL) {
        return NULL;
    }

    xform_matrix xrot, yrot, zrot;
    int currDeg;

    for(int i = 0; i < ROTATION_SIZE; i++) {
        //Allocating space for each molecule
        rotMols->x[i] = molcopy(mol);
        rotMols->y[i] = molcopy(mol);
        rotMols->z[i] = molcopy(mol);

        //Checking if the molcopys worked
        if(rotMols->x[i] == NULL || rotMols->y[i] == NULL || rotMols->z[i] == NULL) {
            
            //Freeing prior malloced memory
            for(int j = 0; j <= i; j++) {
                molfree(rotMols->x[j]);
                molfree(rotMols->y[j]);
                molfree(rotMols->z[j]);
            }

            free(rotMols);
            return NULL;
        }


        currDeg = i*5;

        xrotation(xrot, currDeg);
        yrotation(yrot, currDeg);
        zrotation(zrot, currDeg);

        mol_xform(rotMols->x[i], xrot);
        mol_xform(rotMols->y[i], yrot);
        mol_xform(rotMols->z[i], zrot);
    }

    return rotMols;
}

//Frees the complete rotation struct
void rotationsfree(rotations *rotations) {
    //Freeing each molecule in the rotations struct
    for (int i = 0; i < ROTATION_SIZE; i++) {
        molfree(rotations->x[i]);
        molfree(rotations->y[i]);
        molfree(rotations->z[i]);
    }

    free(rotations);
}
