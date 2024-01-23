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
    
    def is_feasible(self, problem: Problem)-> bool:
        """Indicates wether the solution's hard constraints are respected."""

        # Blocking shifts
        for schedule in self.planning:
            for d in range(1, len(schedule)):
                current_shift = schedule[d]
                previous_shift = schedule[d - 1]
                if current_shift != None and previous_shift != None:
                    if current_shift in problem.shift_types[previous_shift].blocked_shift_types:
                        print("Blocking shifts")
                        return False
            
        # Max shift
        for staff_int in range(len(self.planning)):
            schedule = self.planning[staff_int]
            max_shift_days = problem.staff[staff_int].max_shift_days
            shift_count = [0 for _ in range(len(max_shift_days))]
            for day in schedule:
                if day != None:
                    shift_count[day] += 1
            for i in range(len(shift_count)):
                if shift_count[i] > max_shift_days[i]:
                    print("Max shifts")
                    return False
        
        # Maximum and minimum minutes worked
        for staff_int in range(len(self.planning)):
            schedule = self.planning[staff_int]
            minutes = 0
            for day in schedule:
                if day != None:
                    minutes += problem.shift_types[day].duration
            staff = problem.staff[staff_int]
            if minutes > staff.max_worktime or minutes < staff.min_worktime:
                print("max/min minutes worked")
                return False
        
        # Max/min consecutive shifts and min consecutive days off
        for staff_int in range(len(self.planning)):
            staff = problem.staff[staff_int]
            schedule = self.planning[staff_int].copy()
            while len(schedule) > 0:
                content_type = type(schedule.pop(0))
                count = 1
                while len(schedule) > 0 and type(schedule[0]) == content_type:
                    schedule.pop(0)
                    count += 1
                
                if content_type == type(None):
                    if count < staff.min_consecutive_rest_days:
                        print("min consecutive rest days")
                        return False
                else:
                    if count < staff.min_consecutive_shifts or count > staff.max_consecutive_shifts:
                        print("content :", content_type, "count :", count)
                        print(f"[staff {staff_int}] max/min consecutive shifts")
                        return False
        
        # Max number of weekends
        for staff_int in range(len(self.planning)):
            staff = problem.staff[staff_int]
            schedule = self.planning[staff_int]
            max_weekends = staff.max_worked_weekends
            weekends = []
            for i in range(len(schedule)//7):
                weekends.append((schedule[7*i+5], schedule[7*i+6]))
            for weekend in weekends:
                if weekend[0] != None or weekend[1] != None:
                    max_weekends -= 1
            if max_weekends < 0:
                print("max weekends worked")
                return False
        
        # Requested days off
        for staff_int in range(len(self.planning)):
            staff = problem.staff[staff_int]
            schedule = self.planning[staff_int]
            for rest_day in staff.rest_days:
                if schedule[rest_day] != None:
                    print("requested days off")
                    return False

        return True
            

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
