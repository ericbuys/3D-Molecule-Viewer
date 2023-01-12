#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//Structs
typedef struct atom {
    char element[3];
    double x, y, z;
} atom;

typedef struct bond {
    atom *a1, *a2;
    unsigned char epairs;
} bond;

typedef struct molecule {
    unsigned short atom_max, atom_no;
    atom *atoms, **atom_ptrs;
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
} molecule;

typedef double xform_matrix[3][3];

//Function Prototypes
void atomset(atom *atom, char element[3], double *x, double *y, double *z);
void atomget(atom *atom, char element[3], double *x, double *y, double *z);
void bondset(bond *bond, atom *a1, atom *a2, unsigned char epairs);
void bondget(bond *bond, atom **a1, atom **a2, unsigned char *epairs);
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);
molecule *molcopy(molecule *src);
void molfree(molecule *ptr);
void molappend_atom(molecule *molecule, atom *atom);
void molappend_bond(molecule *molecule, bond *bond);
void molsort(molecule *molecule);
void xrotation(xform_matrix xform_matrix, unsigned short deg);
void yrotation(xform_matrix xform_matrix, unsigned short deg);
void zrotation(xform_matrix xform_matrix, unsigned short deg);
void mol_xform(molecule *molecule, xform_matrix matrix);

//Nightmare Mode
typedef struct rotations {
    molecule *x[72];
    molecule *y[72];
    molecule *z[72];
} rotations;

rotations *spin(molecule *mol);
void rotationsfree(rotations *rotations);
