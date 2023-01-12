#include "mol.h"

//Copys the values in element, x, y, and z into atom
void atomset(atom *atom, char element[3], double *x, double *y, double *z) {
    strcpy(atom->element, element);

    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget(atom *atom, char element[3], double *x, double *y, double *z) {
    strcpy(element, atom->element);

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}
