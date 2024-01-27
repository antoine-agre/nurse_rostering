from nurse_rostering.model.solution import Solution
from nurse_rostering.io.export_solution import Solution2file
from nurse_rostering.io.importer import Importer
from nurse_rostering.Solution.VND_Algo import VND
from nurse_rostering.model.neighborhood import TwoExchangeNeighborhood

infos = [ ("SchedulingPeriodFile","./Instance3.ros"), # chemin absolu | chemin relatif par rapport au fichier solution.
        ("Penalty","521"),
        ("DateFound","12/10/2023"),
        ("FoundBy","Arthur"),
        ("System", "Windows 10 pro"),
        ("CPU","processeur Intel Core i5 2.48Ghz"),
        ("Algorithm","VNS"),
        ("CpuTime","1235.02") ]

problem = Importer().import_problem("nurse_rostering/examples/Instance2.txt")
print(problem)
a = Solution.from_problem(problem)

print(a.planning)

# print(a.value())

# vnd = VND(problem, [TwoExchangeNeighborhood(problem)])

# b = vnd.variable_neighborhood_descent(a)

# print(f"AVANT/APRÈS : {a.value()}/{b.value()}")

# print("B")
# a.generate_solution()
# print(a.planning)



# print()
# print(a.planning)

# print("VALUE :", a.value())

# from nurse_rostering.model.neighborhood import TwoExchangeNeighborhood
# neighborhood = TwoExchangeNeighborhood(problem)
# best_neighbor = neighborhood.best_neighbor(a)

# print("\n\n Best neighbor :")
# print(best_neighbor.planning)

# print("VALUE :", best_neighbor.value())