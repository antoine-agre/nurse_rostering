import xml.etree.ElementTree as ET
import os

# A Verifier
#info : une liste de couple ou de tuple (propriété,valeur)
#
# [ (SchedulingPeriodFile,""../Instance_x.ros""), # chemin absolu | chemin relatif par rapport au fichier solution.
#   ("Penalty","521"),
#   ("DateFound","12/10/2023"),
#   ("FoundBy","Arthur"),
#   ("System", "Windows 10 pro"),
#   (CPU","processeur Intel Core i5 2.48Ghz"),
#   ("Algorithm","VNS"),
#   ("CpuTime","1235.02") ]
#
#planning[staff][day]=shift (None ou un entier)
#int2shiftID : relation entre les shift_id et l'identifiant correspondant dans l'enoncé du probleme
#

""" Export the solution into .ros file """

class Solution2file:

    def __init__(self,int2staffID:list[str],int2shiftID:list[str],planning:list[list[int]],info:list[tuple[str,str]]):
        
        self.int2staffID = int2staffID
        self.int2shiftID = int2shiftID # shift index in the list to match shiftId in the problem
        self.info = info # list of tuple (property,value) of informations about problem resolution 
        self.planning = planning # matrix of solution

    def __info__(self):
        print("Informations about solution processing:")
        for value in self.info:
            print(f"{value[0]} : {value[1]}")
    
    
    def generate_rosterFile(self,baseFolder):
    
        #root of xml (.ros file)
        roster = ET.Element('Roster',attrib = {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance","xsi:noNamespaceSchemaLocation":"Roster.xsd"})
        
        #input info about problem resolution

        relativePath =  os.path.relpath(self.info[0][1], baseFolder) # relative path
        element = ET.SubElement(roster,self[0])
        element.text = relativePath

        for item in self.info[1:]:
            element = ET.SubElement(roster,item[0])
            element.text = item[1]
        
        #input the elements of planning
        nb_employee,nb_day = len(self.planning),len(self.planning[0])
        for staff_id in range(nb_employee):
            for day_id  in range(nb_day):
                shift_id = self.planning[staff_id][day_id]
                if shift_id!=None:

                    employee = ET.SubElement(roster,"Employee",)
                    employee.set("ID",self.int2staffID[staff_id])
                    
                    assign = ET.SubElement(employee,"Assign")
                    day = ET.SubElement(assign,"Day")
                    day.text = str(day_id+1)

                    shift = ET.SubElement(assign,"Shift")
                    shift.text = self.int2shiftID[shift_id]
    
        fileProvider = ET.ElementTree(roster)
        
        #save file
        penality  = self.info[1][1]
        solutionFilename : str = findFilenameWithoutExtension(self.info[0][1])+".Solution."+str(penality)+".ros"
        solutionPath = baseFolder+solutionFilename
        fileProvider.write(solutionPath,encoding="UTF-8",xml_declaration= True)

        
def findFilenameWithoutExtension(path):

    folderSep = os.path.sep
    filename = path.split(folderSep)[-1]
    return filename.split(".")[0]

