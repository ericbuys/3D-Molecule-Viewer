CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all: libmol.so

libmol.so: mol.o
	$(CC) $(CFLAGS) mol.o -shared -o libmol.so

mol.o: mol.c mol.h
	$(CC) $(CFLAGS) -fPIC -c mol.c -o mol.o

#Test 1 created by Professor
test1.o: test1.c mol.h
	$(CC) $(CFLAGS) -c test1.c -o test1.o

test1: test1.o libmol.so
	$(CC) $(CFLAGS) test1.o -L. -lmol -lm -o test1

#Test 2 created by Professor
test2.o: test2.c mol.h
	$(CC) $(CFLAGS) -c test2.c -o test2.o

test2: test2.o libmol.so
	$(CC) $(CFLAGS) test2.o -L. -lmol -lm -o test2

#Test 3 created by Professor
test3: test3.o libmol.so
	$(CC) $(CFLAGS) test3.o -L. -lmol -lm -o test3

test3.o: test3.c mol.h
	$(CC) $(CFLAGS) -c test3.c -o test3.o

#Omega Test
test6.o: test6.c mol.h
	$(CC) $(CFLAGS) -c test6.c -o test6.o

omegaTest: test6.o libmol.so
	$(CC) $(CFLAGS) test6.o -L. -lmol -lm -o omegaTest

clean: 
	rm *.o *.so test1 test2 test3 omegaTest
