from nurse_rostering.model.solution import Solution
from nurse_rostering.io.export_solution import Solution2file
from nurse_rostering.io.importer import Importer
from datetime import datetime
import time

infos = [ ("SchedulingPeriodFile","./Instance3.ros"), # chemin absolu | chemin relatif par rapport au fichier solution.
        ("Penalty","521"),
        ("DateFound","12/10/2023"),
        ("FoundBy","Arthur"),
        ("System", "Windows 10 pro"),
        ("CPU","processeur Intel Core i5 2.48Ghz"),
        ("Algorithm","VNS"),
        ("CpuTime","1235.02") ]

problem = Importer().import_problem("Instance3.txt")
print(problem)
a = Solution.from_problem(problem)

print(a.planning)

s2f = Solution2file(problem, a.planning, infos, "Instance3")
s2f.generate_rosterFile(".")


def info_provider(solution):

        # date du jouts
        date_heure_actuelles = datetime.now()
        date = date_heure_actuelles.strftime("%d/%m/%Y %H:%M:%S")
        authors = "Team @Antoine-@Khaoula-@Giovanni"
        algorithm = "Variable Neighborhood Descent"

        # Convertissez les différences en heures, minutes et secondes
        cpu_hours, cpu_remainder = divmod(solution.cpu_time, 3600)
        cpu_minutes, cpu_seconds = divmod(cpu_remainder, 60)
        cpu_time = "{:02} Heures {:02} minutes {:02} secondes".format(int(cpu_hours), int(cpu_minutes), int(cpu_seconds))

        informations = [
                        ("SchedulingPeriodFile", f"{solution.pathTowardsProblem}"),
                        ("Penality",f"{solution.value()}"),                 
                        ("DateFound",date),
                        ("FoundBy",authors),
                        ("Algorithm",algorithm),
                        ("CpuTime",cpu_time) ]
        
        return informations