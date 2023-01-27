CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: test1 test2

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fpic -c mol.c -o mol.o

test1.o: test1.c mol.h
	$(CC) $(CFLAGS) -c test1.c -o test1.o

test2.o: test2.c mol.h
	$(CC) $(CFLAGS) -c test2.c -o test2.o

test1: test1.o libmol.so
	$(CC) $(CFLAGS) test1.o -L. -lmol -o test1

test2: test2.o libmol.so
	$(CC) $(CFLAGS) test2.o -L. -lmol -o test2

clean: 
	rm *.o *.so test1
