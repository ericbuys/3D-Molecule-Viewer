import os;
import sqlite3;
import MolDisplay;

class Database:
    def __init__(self, reset=False):
        if(reset):
            try:
                newDB = open("molecules.db", "x");
            except FileExistsError:
                os.remove('molecules.db');
                newDB = open("molecules.db", "x");
        
        self.conn = sqlite3.connect("molecules.db");
    
    def create_tables(self):
        conn = self.conn;

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
            conn.execute( """
                            CREATE TABLE Atoms (
                                ATOM_ID         INTEGER         PRIMARY KEY     AUTOINCREMENT   NOT NULL,
                                ELEMENT_CODE    VARCHAR(3)      NOT NULL,
                                X               DECIMAL(7,4)    NOT NULL,
                                Y               DECIMAL(7,4)    NOT NULL,
                                Z               DECIMAL(7,4)    NOT NULL
                            );
                        """ );
        
        try:
            conn.execute("SELECT * FROM Bonds");
        except sqlite3.OperationalError:
            conn.execute( """
                            CREATE TABLE Bonds (
                                BOND_ID     INTEGER     PRIMARY KEY     AUTOINCREMENT   NOT NULL,
                                A1          INTEGER     NOT NULL,
                                A2          INTEGER     NOT NULL,
                                EPAIRS      INTEGER     NOT NULL              
                            );
                        """ );
        
        try:
            conn.execute("SELECT * FROM Molecules");
        except sqlite3.OperationalError:
            conn.execute( """
                            CREATE TABLE Molecules (
                                MOLECULE_ID     INTEGER     PRIMARY KEY     AUTOINCREMENT   NOT NULL,
                                NAME            TEXT        UNIQUE          NOT NULL             
                            );
                        """ );

        try:
            conn.execute("SELECT * FROM MoleculeAtom");
        except sqlite3.OperationalError:
            conn.execute( """
                            CREATE TABLE MoleculeAtom (
                                MOLECULE_ID     INTEGER     NOT NULL,
                                ATOM_ID         INTEGER     NOT NULL,
                                PRIMARY KEY(MOLECULE_ID, ATOM_ID),
                                FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY(ATOM_ID) REFERENCES Atoms    
                            );
                        """ );
        
        try:
            conn.execute("SELECT * FROM MoleculeBond");
        except sqlite3.OperationalError:
            conn.execute( """
                            CREATE TABLE MoleculeBond (
                                MOLECULE_ID     INTEGER     NOT NULL,
                                BOND_ID         INTEGER     NOT NULL,
                                PRIMARY KEY(MOLECULE_ID, BOND_ID),
                                FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules,
                                FOREIGN KEY(BOND_ID) REFERENCES Bonds  
                            );
                        """ );
    
    def __setitem__(self, table, values):
        questionMarkStr = ", ".join(('?',)*len(values)) 
        insertStr = f"INSERT INTO {table} VALUES (" + questionMarkStr + ")";

        self.conn.execute(insertStr, values);
        self.conn.commit();
    
    def add_atom(self, molname, atom):
        #Adding Atom to Atoms Table
        newAtom = MolDisplay.Atom(atom);
        self['Atoms'] = (None, newAtom.atom.element, newAtom.atom.x, newAtom.atom.y, newAtom.atom.z);

        #Retrieving MOLECULE_ID
        molID = self.conn.execute("""
                                    SELECT Molecules.MOLECULE_ID from Molecules 
                                    WHERE NAME = ?
                                """, (molname,));
        molID = molID.fetchall()[0][0];

        #Retrieving ATOM_ID
        atomID = self.conn.execute("""
                                        SELECT Atoms.ATOM_ID from Atoms
                                        WHERE ELEMENT_CODE = ? AND X = ? AND Y = ? AND Z = ?
                                    """, (newAtom.atom.element, newAtom.atom.x, newAtom.atom.y, newAtom.atom.z));
        atomID = atomID.fetchall()[0][0];

        #Adding entry to MoleculeAtom Table
        self['MoleculeAtom'] = (molID, atomID);
    
    def add_bond(self, molname, bond):
        #Adding Bond to Bonds Table
        newBond = MolDisplay.Bond(bond);
        self['Bonds'] = (None, newBond.bond.a1, newBond.bond.a2, newBond.bond.epairs);

        #Retrieving MOLECULE_ID
        molID = self.conn.execute("""
                                    SELECT Molecules.MOLECULE_ID from Molecules 
                                    WHERE NAME = ?
                                """, (molname,));
        molID = molID.fetchall()[0][0];

        #Retrieving BOND_ID
        bondID = self.conn.execute("""
                                        SELECT Bonds.BOND_ID from Bonds
                                        WHERE A1 = ? AND A2 = ? AND EPAIRS = ?
                                    """, (newBond.bond.a1, newBond.bond.a2, newBond.bond.epairs));
        bondID = bondID.fetchall()[0][0];

        #Adding entry to MoleculeAtom Table
        self['MoleculeBond'] = (molID, bondID);
    
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule();
        mol.parse(fp);

        #Insert Entry to Molecules Table
        self['Molecules'] = (None, name)

        #Insert Atoms
        for i in range(mol.atom_no):
            self.add_atom(name, mol.get_atom(i));
        
        #Insert Bonds
        for i in range(mol.bond_no):
            self.add_bond(name, mol.get_bond(i));
        





if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    #connection = sqlite3.connect("molecules.db");
    #print(connection.execute( """SELECT * FROM Elements;""" ).fetchall())
    fp = open( 'water-3D-structure-CT1000292221.sdf' );
    db.add_molecule( 'Water', fp );
    '''
    fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    db.add_molecule( 'Caffeine', fp );
    fp = open( 'CID_31260.sdf' );
    db.add_molecule( 'Isopentanol', fp );
    '''
    # display tables
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );
    


