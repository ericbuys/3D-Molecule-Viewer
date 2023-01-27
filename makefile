CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: test1

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fpic -c mol.c -o mol.o

test1.o: test1.c mol.h
	$(CC) $(CFLAGS) -c test1.c -o test1.o

test1: test1.o libmol.so
	$(CC) $(CFLAGS) test1.o -L. -lmol -o test1

clean: 
	rm *.o *.so test1
