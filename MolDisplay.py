import molecule;

#Constants
radius = { 'H': 25,
           'C': 40,
           'O': 40,
           'N': 40,
         };

element_name = { 'H': 'grey',
                 'C': 'black',
                 'O': 'red',
                 'N': 'blue',
               };

header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";
offsetx = 500;
offsety = 500;

def xCoordSVG(x):
    return x*100.0 + offsetx

def yCoordSVG(y):
    return y*100.0 + offsety

class Atom:
    def __init__(self, atom: molecule.atom):
        self.atom = atom
        self.z = atom.z
    
    def __str__(self):
        return """Element: %s, x: %f, y: %f, z: %f""" % (self.atom.element, self.atom.x, self.atom.y, self.atom.z)
    
    def svg(self):
        xCoord = xCoordSVG(self.atom.x)
        yCoord = yCoordSVG(self.atom.y)
        rad = radius[self.atom.element]
        col = element_name[self.atom.element]

        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="%s"/>\n' % (xCoord, yCoord, rad, col)

class Bond:
    def __init__(self, bond: molecule.bond):
        self.bond = bond
        self.z = bond.z
    
    def __str__(self):
        return """%d %d %d %f %f %f %f %f %f %f""" % (self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.len, self.bond.dx, self.bond.dy)

    def svg(self):
        x11 = xCoordSVG(self.bond.x1) - self.bond.dy*10
        y11 = yCoordSVG(self.bond.y1) - self.bond.dx*10
        x12 = xCoordSVG(self.bond.x1) + self.bond.dy*10
        y12 = yCoordSVG(self.bond.y1) + self.bond.dx*10
        x21 = xCoordSVG(self.bond.x2) - self.bond.dy*10
        y21 = yCoordSVG(self.bond.y2) - self.bond.dx*10
        x22 = xCoordSVG(self.bond.x2) + self.bond.dy*10
        y22 = yCoordSVG(self.bond.y2) + self.bond.dx*10

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x11, y11, x12, y12, x22, y22, x21, y21)

class Molecule(molecule.molecule):
    def __str__(self):
        returnStr = ""
        for i in range(self.atom_no):
            returnStr += "Atom " + i + ": " + Atom(self.get_atom(i)) + "\n";
        for i in range(self.bond_no):
            returnStr += "Bond " + i + ": " + Bond(self.get_bond(i)) + "\n";
        return returnStr


if __name__ == "__main__":
    tempA1 = molecule.atom('H', 1, 2, 3)
    a1 = Atom(tempA1)
    print(a1)
    tempList = []
    tempList.append("hellooooooo")
    tempList.append("joel is kind of a cool person")
    print("".join(tempList))

