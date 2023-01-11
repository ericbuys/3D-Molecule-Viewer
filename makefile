CFLAGS = -std=c99 -Wall -pedantic

libmol.so: mol.o
	gcc mol.o $(CFLAGS) -shared -o libmol.so

mol.o: mol.c mol.h
	gcc $(CFLAGS) -fpic -c mol.c

clean:
	rm *.o *.so
