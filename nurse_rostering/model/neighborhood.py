"""This module defines the neighborhood structures used by the VND,
as defined by Rahimian et al., 2017
"""

from nurse_rostering.model.problem import Problem
from nurse_rostering.model.solution import Solution
from typing import Tuple

class Neighborhood:
    """Interface for implementing neighborhoods structures."""
    
    def __init__(self, problem: Problem) -> None:
        self.problem = problem
    
    def best_neighbor(self, solution: Solution) -> Solution:
        """Return best neighbor of solution in this neighborhood structure."""
        pass


##

# def compare(best_value: int, best_solution: Solution, neighbor: Solution) -> Solution:
#     """Retourne la nouvelle meilleure """


class TwoExchangeNeighborhood(Neighborhood):
    """This neighborhood consists of all moves where two shifts are swapped
    between two different nurses on the same day."""

    def __init__(self, problem: Problem) -> None:
        super().__init__(problem)
    
    def best_neighbor(self, solution: Solution) -> Solution:
        # Variables
        best_solution: Solution = solution
        best_value: int = solution.value()

        # For all staff pairs
        for first_staff_int in range(len(self.problem.staff)):
            for second_staff_int in range(first_staff_int + 1, len(self.problem.staff)):

                # print(f"{first_staff_int}/{second_staff_int}")
                
                first_planning = solution.planning[first_staff_int]
                second_planning = solution.planning[second_staff_int]

                # For all days
                for day in range(self.problem.days_count):

                    #TODO : allow exchanging rest days
                    if first_planning[day] != second_planning[day]:
                        
                        # print("neighbor considered !")
                        neighbor: Solution = solution.deep_copy()
                        neighbor.planning[first_staff_int][day] = second_planning[day]
                        neighbor.planning[second_staff_int][day] = first_planning[day]
                        
                        if neighbor.is_feasible():
                            new_value = neighbor.value()
                            if new_value < best_value:
                                best_value = new_value
                                best_solution = neighbor
        
        return best_solution