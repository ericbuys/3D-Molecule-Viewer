import sys;
import MolDisplay
import io
import molecule;
from http.server import HTTPServer, BaseHTTPRequestHandler;

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        if self.path == "/":
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len(home_page) );
            self.end_headers();
            self.wfile.write( bytes( home_page, "utf-8" ) );
        else:
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: not found", "utf-8" ) );
    
    def do_POST(self):
        if self.path == "/molecule":
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
    

home_page = """
<html>
  <head>
    <title> File Upload </title>
  </head>
  <body>
    <h1> File Upload </h1>
    <form action="molecule" enctype="multipart/form-data" method="post">
    	<p>
        	<input type="file" id="sdf_file" name="filename"/>
     	</p>
		<h2> Apply Rotations </h2>
		<p>
			<label for="pitch">Roll</label>
			<input type="number" id="roll" name="roll"/>
		</p>
		<p>
			<label for="pitch">Pitch</label>
			<input type="number" id="pitch" name="pitch"/>
		</p>
		<p>
			<label for="pitch">Yaw</label>
			<input type="number" id="yaw" name="yaw"/>
    	</p>
		<p>
        	<input type="submit" value="Upload"/>
    	</p>
    </form>
    
  </body>
</html>
""";


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    httpd.serve_forever();
    