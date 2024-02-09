CC = clang
CFLAGS = -Wall -std=c99 -pedantic
#export LD_LIBRARY_PATH=`pwd`

all: libmol.so _molecule.so

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fPIC -c mol.c -o mol.o

_molecule.so: molecule_wrap.o
	$(CC) $(CFLAGS) molecule_wrap.o -lmol -lpython3.10 -L. -L/Library/Frameworks/Python.framework/Versions/3.10/lib -dynamiclib -shared -o _molecule.so

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -fPIC -I/Library/Frameworks/Python.framework/Versions/3.10/include/python3.10/ -c molecule_wrap.c -o molecule_wrap.o

molecule_wrap.c: molecule.i
	swig -python molecule.i

clean: 
	rm *.o *.so molecule_wrap.c molecule.py
