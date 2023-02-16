CC = clang
CFLAGS = -Wall -std=c99 -pedantic
#export LD_LIBRARY_PATH=`pwd`

all: libmol.so

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fPIC -c mol.c -o mol.o

part2Test: part2Test.o libmol.so
	$(CC) $(CFLAGS) part2Test.o -L. -lmol -lm -o part2Test

part2Test.o: part2Test.c mol.h
	$(CC) $(CFLAGS) -c part2Test.c -o part2Test.o

clean: 
	rm *.o *.so part2Test
