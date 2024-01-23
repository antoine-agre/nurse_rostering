import xml.etree.ElementTree as ET
import os

# A Verifier
#info : une liste de couple ou de tuple (propriété,valeur)
#
# [ (SchedulingPeriodFile,""../../problem.txt""),
#   ("Penalty","521"),
#   ("DateFound","12/10/2023"),
#   ("FoundBy","Arthur"),
#   ("System,CPU","processeur Core i5"),
#   ("Algorithm","VNS"),
#   ("CpuTime","1235.02") ]
#
#planning[staff][day]=shift (None ou un entier)
#intToType : relation entre les shift_id et l'identifiant correspondant dans l'enoncé du probleme
#

""" Export the solution into .ros file """

class Solution2file:

    def __init__(self,intToType:list[str],planning:list[list[int]],info:list[tuple[str,str]]):
        
        self.intToType = intToType # shift index in the list to match shiftId in the problem
        self.info = info # list of tuple (property,value) of informations about problem resolution 
        self.planning = planning # matrix of solution

    def __info__(self):
        print("Informations about solution processing:")
        for value in self.info:
            print(f"{value[0]} : {value[1]}")
    
    
    def generate_rosterFile(self):
    
        #root of xml (.ros file)
        roster = ET.Element('Roster',attrib = {"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance","xsi:noNamespaceSchemaLocation":"Roster.xsd"})
        
        #input info about problem resolution
        for item in self.info:
            element = ET.SubElement(roster,f"{item[0]}")
            element.text = item[1]
        
        #input the elements of planning
        nb_employee,nb_day = 1,2
        for staff_id in range(nb_employee):
            for day_id  in range(nb_day):
                shift_id = self.planning[staff_id][day_id]
                if shift_id!=None:

                    employee = ET.SubElement(roster,"Employee",)
                    employee.set("ID","{:0{}}".format(staff_id,nb_employee))
                    
                    assign = ET.SubElement(employee,"Assign")
                    day = ET.SubElement(assign,"Day")
                    day.text = str(day_id)

                    shift = ET.SubElement(assign,"Shift")
                    shift.text = self.intToType[shift_id]
    
        fileProvider = ET.ElementTree(roster)
        
        #save file
        penality  = self.info[1][1]
        solutionFilename : str = findFilenameWithoutExtension(self.info[0][1])+".Solution."+str(penality)+".ros"
        baseFolder = "../solutions/"
        solutionPath = baseFolder+solutionFilename+".Solution."+str(penality)+".ros"
        fileProvider.write(solutionPath,encoding="UTF-8",xml_declaration= True)

        
def findFilenameWithoutExtension(path):

    folderSep = os.path.sep
    filename = path.split(folderSep)[-1]
    return filename.split(".")[0]

