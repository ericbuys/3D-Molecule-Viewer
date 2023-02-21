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

            length = int(self.headers.get('content-length'))
            reader = self.rfile.read(length).decode('utf-8').split("\n")
            wrapper = io.TextIOWrapper(io.BufferedReader(io.BytesIO(bytes(("\n".join(reader[4:])), 'utf-8'))))

            mol = MolDisplay.Molecule()
            mol.parse(wrapper)
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
      <p>
        <input type="submit" value="Upload"/>
      </p>
    </form>
  </body>
</html>
""";

httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
httpd.serve_forever();
