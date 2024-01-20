import xml.etreeElementTree as ET

# A Verifier
#info : une liste de couple ou de tuple (propriété,valeur)
#info : [filname,SchedulingPeriodFile,Penalty,DateFound,FoundBy,System,CPU,Algorithm,CpuTime]
#planning[staff][day]=shift (None ou un entier)
#intToType : relation entre les shift_id et l'identifiant correspondant dans l'enoncé du probleme
#

class Solution:

    def __init__(self,intToType,planning,info= None):
        
        self.intToType:dict[int:str] = intToType
        self.info:list = info
        self.planning:list = planning

    def __info__(self):
        print(type(self.info))
        for value in enumerate(self.info):
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
                    shift.text = str(shift_id)
    
        fileProvider = ET.ElementTree(roster)
        
        #save file
        penality  = self.info[2]
        filename =  self.info[0]
        solutionFilename = filename+".Solution."+str(penality)+".ros"
        fileProvider.write(solutionFilename,encoding="UTF-8",xml_declaration= True)