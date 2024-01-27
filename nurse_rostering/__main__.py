from nurse_rostering.model.solution import Solution
from nurse_rostering.io.export_solution import Solution2file
from nurse_rostering.io.importer import Importer
from nurse_rostering.Solution.VND_Algo import VND
from nurse_rostering.model.neighborhood import TwoExchangeNeighborhood
from datetime import datetime

def info_provider(solution: Solution):

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
                        ("SchedulingPeriodFile", f"../instances/{solution.path_to_problem[:-4]}.ros"),
                        ("Penalty",f"{solution.value()}"),
                        ("DateFound",date),
                        ("FoundBy",authors),
                        ("Algorithm",algorithm),
                        ("CpuTime",cpu_time) ]
        
        return informations

###

problem = Importer().import_problem("Instance4.txt")
print(problem)
a = Solution.from_problem(problem)

print(a.planning)

##### SET THE a.pathTowardsProblem: str BEFORE RUNNING ####
infos =  info_provider(a)
s2f = Solution2file(problem, a, infos)
s2f.generate_rosterFile("./nurse_rostering/examples/solutions/")

vnd = VND(problem, [TwoExchangeNeighborhood(problem)])
b = vnd.variable_neighborhood_descent(a)

infos = info_provider(b)
s2f = Solution2file(problem, b, infos)
s2f.generate_rosterFile("./nurse_rostering/examples/solutions/")
