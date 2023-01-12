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

molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
    molecule *newMol = malloc(sizeof(molecule));

    newMol->atom_max = atom_max;
    newMol->atom_no = 0;
    newMol->bond_max = bond_max;
    newMol->bond_no = 0;

    newMol->atoms = malloc(sizeof(atom) * atom_max);
    newMol->atom_ptrs = malloc(sizeof(atom*) * atom_max);
    for(int i = 0; i < atom_max; i++) {
        newMol->atom_ptrs[i] = &(newMol->atoms[i]);
    }

    newMol->bonds = malloc(sizeof(bond) * bond_max);
    newMol->bond_ptrs = malloc(sizeof(bond*) * bond_max);
    for(int i = 0; i < bond_max; i++) {
        newMol->bonds[i].a1 = malloc(sizeof(atom));
        newMol->bonds[i].a2 = malloc(sizeof(atom));

        newMol->bond_ptrs[i] = &(newMol->bonds[i]);
    }

    return newMol;
}

//??????????
molecule *molcopy(molecule *src) {
    molecule *newMol = molmalloc(src->atom_max, src->bond_max);
    
    newMol->atom_no = src->atom_no;
    newMol->bond_no = src->bond_no;

    return newMol;
}

void molfree(molecule *ptr) {
    free(ptr->atoms);
    free(ptr->atom_ptrs);

    for(int i = 0; i < ptr->bond_max; i++) {
        free(ptr->bonds[i].a1);
        free(ptr->bonds[i].a2);
    }
    free(ptr->bonds);
    free(ptr->bond_ptrs);

    free(ptr);
}
