CC = clang
CFLAGS = -Wall -std=c99 -pedantic
#export LD_LIBRARY_PATH=`pwd`

all: libmol.so _molecule.so

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fPIC -c mol.c -o mol.o

_molecule.so: molecule_wrap.o
	$(CC) $(CFLAGS) molecule_wrap.o -lmol -lpython3.7m -L. -L/usr/lib/python3.7/config-3.7m-x86_64-linux-gnu -dynamiclib -shared -o _molecule.so

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -fPIC -I/usr/include/python3.7m -c molecule_wrap.c -o molecule_wrap.o

part1Test: part1Test.o libmol.so
	$(CC) $(CFLAGS) part1Test.o -L. -lmol -lm -o part1Test

part1Test.o: part1Test.c mol.h
	$(CC) $(CFLAGS) -c part1Test.c -o part1Test.o

part2Test: part2Test.o libmol.so
	$(CC) $(CFLAGS) part2Test.o -L. -lmol -lm -o part2Test

part1Test.o: part1Test.c mol.h
	$(CC) $(CFLAGS) -c part2Test.c -o part2Test.o

clean: 
	rm *.o *.so part1Test
