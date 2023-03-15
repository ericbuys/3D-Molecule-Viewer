import molecule;

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
        self.bond = bond;
        self.z = bond.z;
    
    def __str__(self):
        return """%d: %d %d %d %f %f %f %f %f %f %f""" % (self.z, self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.len, self.bond.dx, self.bond.dy)

    def svg(self):
        x11 = xCoordSVG(self.bond.x1) + self.bond.dy*10
        y11 = yCoordSVG(self.bond.y1) - self.bond.dx*10
        x12 = xCoordSVG(self.bond.x1) - self.bond.dy*10
        y12 = yCoordSVG(self.bond.y1) + self.bond.dx*10
        x21 = xCoordSVG(self.bond.x2) + self.bond.dy*10
        y21 = yCoordSVG(self.bond.y2) - self.bond.dx*10
        x22 = xCoordSVG(self.bond.x2) - self.bond.dy*10
        y22 = yCoordSVG(self.bond.y2) + self.bond.dx*10

        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x11, y11, x12, y12, x22, y22, x21, y21)

class Molecule(molecule.molecule):
    def __str__(self):
        returnStr = ""
        for i in range(self.atom_no):
            returnStr += "Atom %d: %s\n" % (i, Atom(self.get_atom(i)))
        for i in range(self.bond_no):
            returnStr += "Bond %d: %s\n" % (i, Bond(self.get_bond(i)))
        return returnStr
    
    def svg(self):
        tempList = [header]

        i = 0
        j = 0
        while(i < self.atom_no and j < self.bond_no):
            a1 = Atom(self.get_atom(i))
            b1 = Bond(self.get_bond(j))
            if a1.z < b1.z:
                tempList.append(a1.svg())
                i += 1
            else: # b1.z < a1.z
                tempList.append(b1.svg())
                j += 1

        while(i < self.atom_no):
            a1 = Atom(self.get_atom(i))
            tempList.append(a1.svg())
            i += 1
        while(j < self.bond_no):
            b1 = Bond(self.get_bond(j))
            tempList.append(b1.svg())
            j += 1

        
        tempList.append(footer)
        return "".join(tempList)
    
    def parse(self, file):
        fileContents = file.read().split("\n")
        if(len(fileContents) < 4):
            return

        molCounts = fileContents[3].split()
        if(len(molCounts) < 2):
            return

        atomNum = int(molCounts[0])
        bondNum = int(molCounts[1])

        for i in range(atomNum):
            atomContents = fileContents[4 + i].split()
            self.append_atom(atomContents[3], float(atomContents[0]), float(atomContents[1]), float(atomContents[2]))
        for i in range(bondNum):
            bondContents = fileContents[4 + atomNum + i].split()
            self.append_bond(int(bondContents[0]) - 1, int(bondContents[1]) - 1, int(bondContents[2]))

        file.close()
    
    def rotate(self, roll, pitch, yaw):
        self.rotateMol(roll, pitch, yaw)


if __name__ == "__main__":
    file = open("water-3D-structure-CT1000292221.sdf", "r")
    mol = Molecule()
    mol.parse(file)
    molecule.molsort(mol)
    file = open("test.svg", "w")
    file.write(mol.svg())
    file.close()
