import os;
import sqlite3;

class Database:
    def __init__(self, reset=False):
        if(reset):
            try:
                newDB = open("molecules.db", "x");
            except FileExistsError:
                os.remove('molecules.db');
                newDB = open("molecules.db", "x");
        
        self.connection = sqlite3.connect("molecules.db");
    
    def create_tables(self):
        conn = self.connection;

        try:
            conn.execute("SELECT * FROM Elements");
        except sqlite3.OperationalError:
            conn.execute( """
                            CREATE TABLE Elements (
                                ELEMENT_NO      INTEGER         NOT NULL,
                                ELEMENT_CODE    VARCHAR(3)      NOT NULL,
                                ELEMENT_NAME    VARCHAR(32)     NOT NULL,
                                COLOUR1         CHAR(6)         NOT NULL,
                                COLOUR2         CHAR(6)         NOT NULL,
                                COLOUR3         CHAR(6)         NOT NULL,
                                RADIUS          DECIMAL(3)      NOT NULL,
                                PRIMARY KEY     (ELEMENT_CODE)
                            );
                        """ );

        try:
            conn.execute("SELECT * FROM Atoms");
        except sqlite3.OperationalError:
            #Create Elements Table
        
        try:
            conn.execute("SELECT * FROM Bonds");
        except sqlite3.OperationalError:
            #Create Elements Table
        
        try:
            conn.execute("SELECT * FROM Molecules");
        except sqlite3.OperationalError:
            #Create Elements Table
        
        try:
            conn.execute("SELECT * FROM MoleculeAtom");
        except sqlite3.OperationalError:
            #Create Elements Table
        
        try:
            conn.execute("SELECT * FROM MoleculeBond");
        except sqlite3.OperationalError:
            #Create Elements Table



if __name__ == "__main__":
    test = Database();
    test.create_tables();



