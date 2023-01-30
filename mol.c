#include "mol.h"

//Copys the values in element, x, y, and z into atom
void atomset(atom *atom, char element[3], double *x, double *y, double *z) {
    strcpy(atom->element, element);

    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

//Copys the values in atom to element, x, y and z
void atomget(atom *atom, char element[3], double *x, double *y, double *z) {
    strcpy(element, atom->element);

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

//Copys the values in a1, a2 and epairs into bond
void bondset(bond *bond, atom *a1, atom *a2, unsigned char epairs) {
    bond->a1 = a1;
    bond->a2 = a2;
    bond->epairs = epairs;
}

//Copys the values in bond to a1, a2 and epairs
void bondget(bond *bond, atom **a1, atom **a2, unsigned char *epairs) {
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
}

//Allocates space for a molecule
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
    molecule *newMol = malloc(sizeof(molecule));

    if(newMol == NULL) {
        return NULL;
    }

    newMol->atom_max = atom_max;
    newMol->atom_no = 0;
    newMol->bond_max = bond_max;
    newMol->bond_no = 0;

    newMol->atoms = malloc(sizeof(atom) * atom_max);
    newMol->atom_ptrs = malloc(sizeof(atom*) * atom_max);
   
    if((newMol->atoms == NULL) || (newMol->atom_ptrs == NULL)) {
        return NULL;
    } 

    for(int i = 0; i < atom_max; i++) {
        newMol->atom_ptrs[i] = &(newMol->atoms[i]);
    }

    newMol->bonds = malloc(sizeof(bond) * bond_max);
    newMol->bond_ptrs = malloc(sizeof(bond*) * bond_max);
    
    if((newMol->bonds == NULL) || (newMol->bond_ptrs == NULL)) {
        return NULL;
    }

    for(int i = 0; i < bond_max; i++) {
        newMol->bond_ptrs[i] = &(newMol->bonds[i]);
    }

    return newMol;
}

/*
copy contents of arrays insie molecule asweel (atoms and bonds array not the _ptr ones)
*/
molecule *molcopy(molecule *src) {
    molecule *newMol = molmalloc(src->atom_max, src->bond_max);
    if(newMol == NULL) {
        return NULL;
    }

    for(int i = 0; i < src->atom_no; i++) {
        molappend_atom(newMol, &(src->atoms[i]));
    }

    for(int i = 0; i < src->bond_no; i++) {
        molappend_bond(newMol, &(src->bonds[i]));
    }

    return newMol;
}

void molfree(molecule *ptr) {
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    free(ptr);
}

void molappend_atom(molecule *molecule, atom *atom) {
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
            exit(1);
        } else {
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
            exit(1);
        } else {
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

void molsort(molecule *molecule) {
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), atom_cmp);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), bond_cmp);
}

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

int bond_cmp(const void *a, const void *b) {
    bond *a_ptr, *b_ptr;
    
    a_ptr = *(struct bond **)a;
    b_ptr = *(struct bond **)b;

    double a_ptrAvg = (a_ptr->a1->z + a_ptr->a2->z)/2;
    double b_ptrAvg = (b_ptr->a1->z + b_ptr->a2->z)/2;

    if(a_ptrAvg > b_ptrAvg) {
        return 1;
    } else if (a_ptrAvg == b_ptrAvg) {
        return 0;
    } else {
        return -1;
    }
}

double degToRad(unsigned short deg) {
    return deg * PI / 180;
}

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
}
