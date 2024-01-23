from nurse_rostering.model.solution import Solution
from nurse_rostering.io.export_solution import Solution2file
from nurse_rostering.io.importer import Importer

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