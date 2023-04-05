import sys;
import MolDisplay;
import molsql;
import io;
from io import StringIO;
import molecule;
import urllib;
import json;
from http.server import HTTPServer, BaseHTTPRequestHandler;

public_files = ['/index.html', '/elements.html', '/molecules.html', '/navbar.html', '/viewer.html', '/style.css', '/script.js', '/elements.json'];
server_requests = ['/database-elements', '/database-molecules', '/load-molecule'];

db = molsql.Database(reset=False);
db.create_tables();

selected_molecule = '';

class MyHandler( BaseHTTPRequestHandler ):

    def do_GET(self):
        print(self.path);

        if (self.path in public_files) or (self.path in server_requests):
            self.send_response( 200 ); # OK

            if self.path.endswith('.html'):
                contentType = "text/html"; 
                fp = open("html" + self.path);
            elif self.path.endswith('.css'):
                contentType = "text/css"; 
                fp = open("css" + self.path);
            elif self.path.endswith(".js"):
                contentType = "text/javascript";
                fp = open("js" + self.path);
            elif self.path.endswith(".json"):
                contentType = "application/json";
                fp = open("assets" + self.path)
            elif self.path in server_requests:
                contentType = "text/plain";
            
            if self.path in public_files:
                content = fp.read();
            elif self.path in server_requests:
                if self.path == '/database-elements':
                    content = db.conn.execute( "SELECT Elements.ELEMENT_NO FROM Elements;" ).fetchall();

                    #Create String of Element Numbers to send to HTML page
                    contentList = []
                    for element in content:
                        contentList.append(element[0])
                    content = ','.join(map(str, contentList));

                elif self.path == '/database-molecules':
                    molecule_list = []
                    molecules = db.conn.execute( "SELECT * FROM Molecules;" ).fetchall();

                    for molecule in molecules:
                        molecule_dict = {}
                        
                        molecule_atoms = db.conn.execute("""    SELECT * FROM MoleculeAtom
                                                                WHERE MoleculeAtom.MOLECULE_ID = ?
                                                        """, ((molecule[0]),)).fetchall();


                        molecule_bonds = db.conn.execute("""    SELECT * FROM MoleculeBond
                                                                WHERE MoleculeBond.MOLECULE_ID = ?
                                                        """, ((molecule[0]),)).fetchall();
                        
                        molecule_dict['name'] = molecule[1];
                        molecule_dict['num_atoms'] = len(molecule_atoms);
                        molecule_dict['num_bonds'] = len(molecule_bonds);

                        molecule_list.append(molecule_dict);
                    
                    content = json.dumps(molecule_list);
                
                elif self.path == '/load-molecule':
                    MolDisplay.radius = db.radius();
                    MolDisplay.element_name = db.element_name();
                    MolDisplay.radial_gradients = db.radial_gradients();

                    mol = db.load_mol(selected_molecule);
                    mol.sort()
                    content = mol.svg();
            
            self.send_header( "Content-type", contentType);
            self.send_header( "Content-length", len(content));
            self.end_headers();
            self.wfile.write( bytes( content, "utf-8" ) );
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );
    
    def do_POST(self):
        if self.path == "/add-element":
            #Reading Data that was sent
            content_length = int(self.headers['Content-Length']);
            data = self.rfile.read(content_length);
            data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );
            
            #Adding Element to Database
            db_entry = (int(data['number'][0]), data['symbol'][0], data['name'][0], data['colour1'][0][1:], data['colour2'][0][1:], data['colour3'][0][1:], int(data['radius'][0]));
            db['Elements'] = db_entry;

            #Sending Response to Page
            self.send_response(200); # OK
            self.end_headers();

        elif self.path == "/remove-element":
            #Reading Data that was sent
            content_length = int(self.headers['Content-Length']);
            data = self.rfile.read(content_length);
            data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );
            
            db.conn.execute("""
                                DELETE FROM Elements
                                WHERE Elements.ELEMENT_NO = ?
                                """, ((data['number'][0]),));
            #db.conn.commit();

            #Sending Response to Page
            self.send_response(200);
            self.end_headers();
        
        elif self.path == '/upload-sdf':
            #Reading Data that was sent
            content_length = int(self.headers['Content-Length']);
            data = self.rfile.read(content_length);
            data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );

            db.add_molecule(data['file_name'][0], StringIO(data['file_contents'][0]));

            self.send_response(200)
            self.end_headers()

        elif self.path == '/select-molecule':
            #Reading Data that was sent
            content_length = int(self.headers['Content-Length']);
            data = self.rfile.read(content_length);
            data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );

            global selected_molecule 
            selected_molecule = data['molecule_name'][0]

            self.send_response(200)
            #self.send_header("Content-type", "text/html")
            self.end_headers()
            #self.wfile.write(bytes(mol.svg(), "utf-8"))    
        
        elif self.path == '/rotate-mol':
            #Reading Data that was sent
            content_length = int(self.headers['Content-Length']);
            data = self.rfile.read(content_length);
            data = urllib.parse.parse_qs( data.decode( 'utf-8' ) );

            MolDisplay.radius = db.radius();
            MolDisplay.element_name = db.element_name();
            MolDisplay.radial_gradients = db.radial_gradients();

            mol = db.load_mol(selected_molecule);
            mol.rotate(int(data['roll'][0]), int(data['pitch'][0]), int(data['yaw'][0]))
            mol.sort()

            content = mol.svg();
            contentType = "text/plain";

            self.send_response(200)
            self.send_header( "Content-type", contentType);
            self.send_header( "Content-length", len(content));
            self.end_headers();
            self.wfile.write( bytes( content, "utf-8" ) );
            
        elif self.path == "/molecule":
            self.send_response(200)
            self.send_header("Content-type", "image/svg+xml")
            self.end_headers()

            #Reading sdf file
            length = int(self.headers.get('content-length'))
            reader = self.rfile.read(length).decode('utf-8').split("\n")
            wrapper = io.TextIOWrapper(io.BufferedReader(io.BytesIO(bytes(("\n".join(reader[4:])), 'utf-8'))))

            #Parsing sdf file
            mol = MolDisplay.Molecule()
            mol.parse(wrapper)

            #Apply rotation to molecule
            if(mol.atom_no != 0 or mol.bond_no != 0):
                defaultOffset = 10 + mol.atom_no + mol.bond_no
                rollOffset = defaultOffset + 4
                pitchOffset = rollOffset + 4
                yawOffset = pitchOffset + 4
                
                try:
                    roll = int(reader[rollOffset])
                except ValueError:
                    roll = 0
                
                try:
                    pitch = int(reader[pitchOffset])
                except ValueError:
                    pitch = 0
                
                try:
                    yaw = int(reader[yawOffset])
                except ValueError:
                    yaw = 0

                mol.rotate(roll, pitch, yaw)

            #Outputting molecule to server
            molecule.molsort(mol)
            self.wfile.write(bytes(mol.svg(), "utf-8"))   

        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );
    

if __name__ == "__main__":
    # db = molsql.Database(reset=True);
    # db.create_tables();
    # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    # db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    # db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    # db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    #MolDisplay.element_name = db.element_name();
    #MolDisplay.header += db.radial_gradients();
    #MolDisplay.radius = db.radius();
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    httpd.serve_forever();
    