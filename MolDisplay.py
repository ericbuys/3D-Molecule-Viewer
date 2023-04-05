import molecule;
import math;

nightmareMode = True;
radial_gradients = '';
header = """<svg version="1.1" width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg>""";
offsetx = 500;
offsety = 500;
DEFAULT_RADIUS = 40;

def xCoordSVG(x):
    return x*100.0 + offsetx

def yCoordSVG(y):
    return y*100.0 + offsety

def distance(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

class Atom:
    def __init__(self, atom: molecule.atom):
        self.atom = atom
        self.z = atom.z
    
    def __str__(self):
        return """Element: %s, x: %f, y: %f, z: %f""" % (self.atom.element, self.atom.x, self.atom.y, self.atom.z)
    
    def svg(self):
        xCoord = xCoordSVG(self.atom.x)
        yCoord = yCoordSVG(self.atom.y)
        rad = radius.get(self.atom.element, DEFAULT_RADIUS)
        
        try:
            col = element_name[self.atom.element]
        except KeyError:
            col = element_name["DEFAULT"];

        return '  <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (xCoord, yCoord, rad, col)

class Bond:
    def __init__(self, bond: molecule.bond):
        self.bond = bond;
        self.z = bond.z;
    
    def __str__(self):
        return """%d: %d %d %d %f %f %f %f %f %f %f""" % (self.z, self.bond.a1, self.bond.a2, self.bond.epairs, self.bond.x1, self.bond.y1, self.bond.x2, self.bond.y2, self.bond.len, self.bond.dx, self.bond.dy)

    #SVG method for non-nightmare mode
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

    #SVG Method for Nightmare Mode
    def specialSVG(self, bondIndex):
        bondWidth = 15;

        #Retrieving Essential Bond Data
        atom1 = self.bond.get_atom(self.bond.a1)
        atom2 = self.bond.get_atom(self.bond.a2)
        atom1Radius = radius.get(atom1.element, DEFAULT_RADIUS)
        atom2Radius = radius.get(atom2.element, DEFAULT_RADIUS)

        #Updating Radius to Make Bond Fill Empty Space
        atom1Radius = math.sqrt(atom1Radius*atom1Radius - bondWidth*bondWidth)
        atom2Radius = math.sqrt(atom2Radius*atom2Radius - bondWidth*bondWidth)

        #Organizing Line Points and Offsets for Increasing Values of X
        if(self.bond.x1 < self.bond.x2):
            p1 = [self.bond.x1, self.bond.y1, atom1.z]
            p2 = [self.bond.x2, self.bond.y2, atom2.z]
        else:
            p1 = [self.bond.x2, self.bond.y2, atom2.z]
            p2 = [self.bond.x1, self.bond.y1, atom1.z]
            temp = atom1Radius;
            atom1Radius = atom2Radius;
            atom2Radius = temp;
        
        #Computing the Unit Vector from P1 to P2
        vectorLen = math.sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2) + pow(p2[2] - p1[2], 2))
        vector = [(p2[0] - p1[0])/vectorLen, (p2[1] - p1[1])/vectorLen, (p2[2] - p1[2])/vectorLen]
        
        #Converting P! and P2 to SVG Coords
        p1[0] = xCoordSVG(p1[0]);
        p2[0] = xCoordSVG(p2[0]);
        p1[1] = yCoordSVG(p1[1]);
        p2[1] = yCoordSVG(p2[1]);

        #Upating P1 and P2 to account for Z value Offsets
        p1[1] += vector[1] * atom1Radius 
        p2[1] -= vector[1] * atom2Radius 
        p1[0] += vector[0] * atom1Radius
        p2[0] -= vector[0] * atom2Radius

        #Turning points for a line to points for a Rectangle
        x11 = p1[0] + self.bond.dy*bondWidth
        y11 = p1[1] - self.bond.dx*bondWidth
        x12 = p1[0] - self.bond.dy*bondWidth
        y12 = p1[1] + self.bond.dx*bondWidth
        x21 = p2[0] + self.bond.dy*bondWidth
        y21 = p2[1] - self.bond.dx*bondWidth
        x22 = p2[0] - self.bond.dy*bondWidth
        y22 = p2[1] + self.bond.dx*bondWidth

        cylinderSVG = '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="url(#bond%d)"/>\n' % (x11, y11, x12, y12, x22, y22, x21, y21, bondIndex)
        
        #Getting Points for Ellipse
        ellipse = []
        pointsForAngle = []
        if(p1[2] < p2[2]):
            ellipse = [p1[0], p1[1]]
            pointsForAngle = [x12, y12]
        else:
            ellipse = [p2[0], p2[1]]
            pointsForAngle = [x22, y22]

        #Computing Axis to be Scaled
        scaledAxis = abs(bondWidth * vector[2]);
        
        #Angle to Rotate Ellipse
        adj = ellipse[0] - pointsForAngle[0]
        hyp = distance(ellipse[0], ellipse[1], pointsForAngle[0], pointsForAngle[1])
        theta = math.degrees(math.acos(adj/hyp))
        if(pointsForAngle[1] > ellipse[1]):
            theta *= -1;

        ellipseSVG = '   <ellipse cx="%.2f" cy="%.2f" rx="%.2f" ry="%.2f" transform="rotate(%.2f, %.2f, %.2f)" fill="url(#cap%d)"/>\n' % (ellipse[0], ellipse[1], bondWidth, scaledAxis, theta, ellipse[0], ellipse[1], bondIndex)

        #Determining Which Gradient Colours To Use and how to Draw the Gradient
        stopColours = []
        gradPoints = []
        
        #Accounting for divide by zero
        if((p2[0]-p1[0]) == 0):
            slope = p2[1] - p1[1]
        else:
            slope = (p2[1] - p1[1])/(p2[0]-p1[0])

        if(slope < 0):
            stopColours = ['#454545', '#606060', '#454545', '#252525']
            if(y11 > y12):
                gradPoints = [x12, y12, x11, y11]
            else:
                gradPoints = [x11, y11, x12, y12] 
        else:
            stopColours = ["#252525", "#404040", "#252525", '#050505']
            gradPoints = [x12, y12, x11 + 2*(self.bond.dy*bondWidth), y11 - 2*(self.bond.dx*bondWidth)] 

        cylinderGradient = f""" <linearGradient id="bond{bondIndex}" x1="{gradPoints[0]:.2f}" y1="{gradPoints[1]:.2f}" x2="{gradPoints[2]:.2f}" y2="{gradPoints[3]:.2f}" gradientUnits="userSpaceOnUse">
                                    <stop offset="0%" stop-color="{stopColours[0]}" />
                                    <stop offset="25%" stop-color="{stopColours[1]}" />
                                    <stop offset="50%" stop-color="{stopColours[2]}" />
                                    <stop offset="100%" stop-color="{stopColours[3]}" />
                                </linearGradient>\n"""

        theta *= -1;
        ellipseGradient = f"""  <linearGradient id="cap{bondIndex}" x1="{gradPoints[0]:.2f}" y1="{gradPoints[1]:.2f}" x2="{gradPoints[2]:.2f}" y2="{gradPoints[3]:.2f}" gradientUnits="userSpaceOnUse" gradientTransform="rotate({theta:.2f},{ellipse[0]:.2f},{ellipse[1]:.2f})">
                                    <stop offset="0%" stop-color="{stopColours[0]}" />
                                    <stop offset="25%" stop-color="{stopColours[1]}" />
                                    <stop offset="50%" stop-color="{stopColours[2]}" />
                                    <stop offset="100%" stop-color="{stopColours[3]}" />
                                </linearGradient>\n"""

        return cylinderGradient + ellipseGradient + cylinderSVG + ellipseSVG;

class Molecule(molecule.molecule):
    def __str__(self):
        returnStr = ""
        for i in range(self.atom_no):
            returnStr += "Atom %d: %s\n" % (i, Atom(self.get_atom(i)))
        for i in range(self.bond_no):
            returnStr += "Bond %d: %s\n" % (i, Bond(self.get_bond(i)))
        return returnStr
    
    def svg(self):
        updatedHeader = header + radial_gradients;
        tempList = [updatedHeader]

        i = 0
        j = 0
        while(i < self.atom_no and j < self.bond_no):
            a1 = Atom(self.get_atom(i))
            b1 = Bond(self.get_bond(j))
            if a1.z < b1.z:
                tempList.append(a1.svg())
                i += 1
            else: # b1.z < a1.z
                bondStr = ""
                if(nightmareMode):
                    bondStr = b1.specialSVG(j);
                else:
                    bondStr = b1.svg()
                
                tempList.append(bondStr);
                j += 1

        while(i < self.atom_no):
            a1 = Atom(self.get_atom(i))
            tempList.append(a1.svg())
            i += 1
        while(j < self.bond_no):
            b1 = Bond(self.get_bond(j))

            bondStr = ""
            if(nightmareMode):
                bondStr = b1.specialSVG(j);
            else:
                bondStr = b1.svg()

            tempList.append(bondStr)
            j += 1

        
        tempList.append(footer)
        return "".join(tempList)
    
    def parse(self, file):
        fileContents = file.read().split("\n")
        print(fileContents)
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
    print("You are in the Main function for MolDisplay.py")
    # file = open("water-3D-structure-CT1000292221.sdf", "r")
    # mol = Molecule()
    # mol.parse(file)
    # molecule.molsort(mol)
    # file = open("test.svg", "w")
    # file.write(mol.svg())
    # file.close()
