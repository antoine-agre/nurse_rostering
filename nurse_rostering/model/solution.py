from nurse_rostering.model.problem import Problem, Staff
from nurse_rostering.io.importer import Importer
from typing import List, Union, Optional

Planning = List[List[Optional[int]]]

class Solution:
    # planning: dict[int, dict[int, dict[int, bool]]]
    # planning: list[list[list[bool]]]
    # planning: list[list[int]]
    # planning[staff][jour] == int
    # self.planning: list[list[int]] #planning[staff][jour] = int de shift ou None

    def __init__(self, planning: Planning) -> None:
        self.planning = planning
        # self.problem: Problem = problem
        self.greedy_initialize(problem)
    
    @classmethod
    def from_problem(cls, problem: Problem):
        planning: Planning = [[None for _ in range(problem.days_count)] for _ in range(len(problem.staff))]
        return cls(planning)
    
    def greedy_initialize(self, problem: Problem)-> None:
        #TODO: select random staff order
        for staff_int in range(len(problem.staff)):
            staff: Staff = problem.staff[staff_int]
            schedule: List[Union[int, bool, None]] = self.planning[staff_int]
            
            # (days off are set as False and worked days as True in planning)

            # SetDaysOff()
            for d in range(problem.days_count):
                schedule[d] = not d in staff.rest_days

            # AssignWorkDays()
            min_work_days = staff.min_consecutive_shifts
            max_work_days = staff.max_consecutive_shifts
            min_rest_days = staff.min_consecutive_rest_days



problem: Problem = Importer().import_problem("Instance2.txt")
# sol: Solution = Solution(problem)
# print(sol.planning)


a = Solution.from_problem(problem)