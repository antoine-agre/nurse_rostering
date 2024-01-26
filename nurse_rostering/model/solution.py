from nurse_rostering.model.problem import Problem, Staff, ShiftType
from nurse_rostering.io.importer import Importer
from typing import List, Union, Optional, Any
from random import random, randint, randrange
from copy import deepcopy

# None = day off, int = shift
Planning = List[List[Optional[int]]]
PersonnalSchedule = List[Optional[int]]

class Solution:
    # planning: dict[int, dict[int, dict[int, bool]]]
    # planning: list[list[list[bool]]]
    # planning: list[list[int]]
    # planning[staff][jour] == int
    # self.planning: list[list[int]] #planning[staff][jour] = int de shift ou None

    def __init__(self, planning: Planning, problem: Problem) -> None:
        self.planning: Planning = planning
        self.problem: Problem = problem
        self.greedy_initialize()
    
    def deep_copy(self):
        return Solution(deepcopy(self.planning), self.problem)

    @classmethod
    def from_problem(cls, problem: Problem):
        planning: Planning = [[None for _ in range(problem.days_count)] for _ in range(len(problem.staff))]
        return cls(planning, problem)
    
    def is_feasible(self)-> bool:
        """Indicates wether the solution's hard constraints are respected."""

        for staff_int in range(len(self.problem.staff)):
            schedule: PersonnalSchedule = self.planning[staff_int]
            if is_personal_schedule_feasible(schedule, self.problem, staff_int) == False:
                return False
        
        return True

    def value(self):
        
        cover_abovePenality = 0
        cover_belowPenality = 0
        shift_avoidedPenality = 0
        shift_wishedPenality = 0

        staff = self.problem.staff
        shift_types = self.problem.shift_types
        planning = self.planning
        
        #penality about staff requirements
        for i_shift in range(len(shift_types)):
            for i_day in range(len(planning[0])):

                diff_s = sum(assign == i_shift for assign in [employee[i_day] for employee in planning]) - shift_types[i_shift].staff_requirements[i_day]
                if diff_s >0:
                    cover_abovePenality += diff_s * shift_types[i_shift].cover_above_penalties[i_day]
                else:
                    cover_belowPenality += (-diff_s) * shift_types[i_shift].cover_below_penalties[i_day]
        
        # Section Request
        for i_employee in range(len(staff)):
            for i_day in range(self.problem.days_count):
                for i_shift in range(len(shift_types)):

                    # penality for shifts off requests 
                    off_penality = staff[i_employee].shift_avoid_penalties[i_day][i_shift]
                    if off_penality != None and planning[i_employee][i_day] == i_shift:
                        shift_avoidedPenality += off_penality

                    # penality for shifts on requests 
                    on_penality = staff[i_employee].shift_wish_penalties[i_day][i_shift]
                    if on_penality != None and planning[i_employee][i_day] != i_shift:
                        shift_wishedPenality += on_penality
        
        return cover_abovePenality + cover_belowPenality + shift_avoidedPenality + shift_wishedPenality

    def greedy_initialize(self)-> None:
        
        while not self.is_feasible():

            print("\tloop")

            staff_ints = [i for i in range(len(self.problem.staff))]
            staff_order = []
            while len(staff_ints) > 0:
                staff_order.append(staff_ints.pop(randrange(len(staff_ints))))

            for staff_int in staff_order:
                print("\r", staff_order.index(staff_int), "/", len(staff_order), end="")
                staff: Staff = self.problem.staff[staff_int]
                schedule: Optional[PersonnalSchedule] = self.planning[staff_int].copy()
                conditions = False
                
                # (days off are None, days worked are set as -1)

                count = 0

                while conditions != True:
                    # SetDaysOff()
                    schedule = set_days_off(self.problem, staff, schedule)

                    # AssignWorkDays()
                    schedule = assign_work_days(staff, schedule)

                    # TODO evaluate weekends ?

                    #AssignShifts()
                    while -1 in schedule:
                        # print("count")
                        schedule = assign_shifts(self.problem, staff, schedule)
                        count += 1
                        if count > 100:
                            break
                    if count > 100:
                        break

                    # print(f"[{staff_int}]", schedule)
                    conditions = evaluate_weekend(staff, schedule) and evaluate_workload(self.problem, staff, schedule)
                
                if count > 100:
                    # count = 0
                    break

                # if schedule == None: break
                self.planning[staff_int] = schedule
            

def is_personal_schedule_feasible(schedule: PersonnalSchedule, 
                                  problem: Problem, staff_int: int) -> bool:
    """Indicates wether the personal schedule's hard constraints are respected."""
    
    # Variables
    staff: Staff = problem.staff[staff_int]

    # Check -1 values
    for day in schedule:
        if day == -1:
            return False

    # Blocking shifts
    for d in range(1, len(schedule)):
        current_shift = schedule[d]
        previous_shift = schedule[d - 1]
        if current_shift != None and previous_shift != None:
            if current_shift in problem.shift_types[previous_shift].blocked_shift_types:
                # print("Blocking shifts")
                return False
        
    # Max shift
    max_shift_days = staff.max_shift_days
    shift_count = [0 for _ in range(len(max_shift_days))]
    for day in schedule:
        if day != None:
            shift_count[day] += 1
    for i in range(len(shift_count)):
        if shift_count[i] > max_shift_days[i]:
            # print("Max shifts")
            return False
    
    # Maximum and minimum minutes worked
    minutes = 0
    for day in schedule:
        if day != None:
            minutes += problem.shift_types[day].duration
    if minutes > staff.max_worktime or minutes < staff.min_worktime:
        # print("max/min minutes worked")
        return False
    
    # Max/min consecutive shifts and min consecutive days off
    schedule_copy = deepcopy(schedule)

    while len(schedule_copy) > 0:
        content_type = type(schedule_copy.pop(0))
        count = 1
        while len(schedule_copy) > 0 and type(schedule_copy[0]) == content_type:
            schedule_copy.pop(0)
            count += 1
        
        if content_type == type(None) and count < staff.min_consecutive_rest_days:
            # print("min consecutive rest days")
            return False
        elif count < staff.min_consecutive_shifts or count > staff.max_consecutive_shifts:
            # print("content :", content_type, "count :", count)
            # print(f"[staff {staff_int}] max/min consecutive shifts")
            return False
    
    # Max number of weekends
    max_weekends = staff.max_worked_weekends
    weekends = []
    for i in range(len(schedule)//7):
        weekends.append((schedule[7*i+5], schedule[7*i+6]))
    for weekend in weekends:
        if weekend[0] != None or weekend[1] != None:
            max_weekends -= 1
    if max_weekends < 0:
        # print("max weekends worked")
        return False
    
    # Requested days off
    for rest_day in staff.rest_days:
        if schedule[rest_day] != None:
            # print("requested days off")
            return False

    return True


def set_days_off(problem: Problem, staff: Staff, schedule: PersonnalSchedule) -> PersonnalSchedule:
    for d in range(problem.days_count):
        if d in staff.rest_days:
            schedule[d] = None
        else:
            schedule[d] = -1
    return schedule

def assign_work_days(staff: Staff, schedule: PersonnalSchedule) -> PersonnalSchedule:
    # Constraints 
    max_shifts = staff.max_consecutive_shifts
    min_shifts = staff.min_consecutive_shifts
    min_off_days = staff.min_consecutive_rest_days

    while not _check_work_days_constraints(schedule, max_shifts, min_shifts, min_off_days):
        
        schedule = _fix_min_work_days(schedule, min_shifts)
        schedule = _fix_min_off_days(schedule, min_off_days)
        schedule = _fix_max_work_days(schedule, max_shifts, min_shifts, min_off_days)
    #     print(schedule)

    # print("DONE :")
    # print(schedule)

    # print("Off days :", schedule.count(None))
    # print("Work days :", schedule.count(-1))

    # 
        
    
    return schedule

# Replace worked day blocks below minimum size by rest days
def _fix_min_work_days(schedule: PersonnalSchedule, min_shifts: int) -> PersonnalSchedule:
    start: Any = None
    end: Any = None
    for i in range(len(schedule)):
        if start == None:
            if schedule[i] == -1:
                start = i
        if start != None:
            if i == len(schedule)-1 or schedule[i+1] != -1:
                end = i
                if (end - start + 1) < min_shifts:
                    for j in range(start, end + 1):
                        schedule[j] = None
                start, end = None, None
    return schedule

# Randomly extend off day blocks below minimum size
def _fix_min_off_days(schedule: PersonnalSchedule, min_off_days: int) -> PersonnalSchedule:
    start, end = None, None
    for i in range(len(schedule)):
        if start == None:
            if schedule[i] == None:
                start = i
        if start != None:
            if i == len(schedule)-1 or schedule[i+1] != None:
                end = i

                if (end - start + 1) < min_off_days:
                    for _ in range(min_off_days - (end - start + 1)):
                        toss = random() > 0.5
                        if end == len(schedule) - 1 or toss:
                            schedule[start-1] = None
                            start -= 1
                        elif start == 0 or not toss:
                            schedule[end+1] = None
                            end += 1

                start, end = None, None
    return schedule

# Randomly add off days to work day blocks above max size
def _fix_max_work_days(schedule: PersonnalSchedule, max_shifts: int, min_shifts: int, min_off_days: int) -> PersonnalSchedule:
    start: Any = None
    end: Any = None
    for i in range(len(schedule)):
        if start == None:
            if schedule[i] == -1:
                start = i
        if start != None:
            if i == len(schedule)-1 or schedule[i+1] != -1:
                end = i
                length = (end - start + 1)
                if length > max_shifts:
                    schedule[randint(start, end)] = None
                    # if length < (2 * min_shifts + min_off_days):
                    #     for _ in range(max_shifts - length):
                    #         if random() > 0.5:
                    #             schedule[start] = None
                    #             start += 1
                    #         else:
                    #             schedule[end] = None
                    #             end -= 1
                    # else:
                start, end = None, None
    return schedule

# Returns true if work days constraints are followed
def _check_work_days_constraints(schedule: PersonnalSchedule, max_shifts: int, min_shifts: int, min_off_days: int) -> bool:
    s = schedule.copy()
    while len(s) > 0:
        length: int = 0
        content: Any = s[0]
        while len(s) > 0 and s[0] == content:
            s.pop(0)
            length += 1

        if content == None: #off day
            if length < min_off_days:
                return False
        elif content == -1: #work day
            if length < min_shifts or length > max_shifts:
                return False
    return True


def assign_shifts(problem: Problem, staff: Staff, schedule: PersonnalSchedule) -> Optional[PersonnalSchedule]:
    # shifts_left: int = schedule.count(-1)
    shifts_left = staff.max_shift_days.copy()
    schedule_copy = schedule.copy()
    loops_without_assignment = 0

    while schedule_copy.count(-1) > 0:
        
        if loops_without_assignment > 100:
            shifts_left = staff.max_shift_days.copy()
            schedule_copy = schedule.copy()
            loops_without_assignment = 0
        # print(schedule_copy)
        # print("left :", shifts_left)

        # random shift still available
        available_shifts = [i for (i, left) in enumerate(shifts_left) if left > 0]
        shift_int = available_shifts[randrange(len(available_shifts))]
        # print("trying for shift", shift_int)

        # random non-assigned, non-blocking day
        available_days = [i for (i, elem) in enumerate(schedule_copy) if elem == -1]
        day_int: Optional[int] = None

        # try to find valid day; after 100 tries, picks new shift
        for _ in range(100):
            day_int = available_days[randrange(len(available_days))]
            # print("picked day", day_int)
            if day_int > 0: # check previous shift, blocking this one
                blocking_shift = schedule_copy[day_int-1]
                if blocking_shift != None and blocking_shift >= 0:
                    if shift_int in problem.shift_types[blocking_shift].blocked_shift_types:
                        # print(f"shift {shift_int} blocked by {blocking_shift}")
                        day_int = None
                        # print(f"blocked by previous shift ({blocking_shift})")
            if day_int != None and day_int < len(schedule_copy) - 1: # check next shift, blocked by this one
                blocked_shift = schedule_copy[day_int+1]
                if blocked_shift != None and blocked_shift >= 0:
                    if blocked_shift in problem.shift_types[shift_int].blocked_shift_types:
                        # print(f"shift {shift_int} blocking {blocked_shift}")
                        day_int = None
                        # print(f"blocking next shift ({blocked_shift})")
            if day_int != None: break

        if day_int == None:
            # print("not fitting")
            loops_without_assignment += 1
            continue

        # print("fitting")
        schedule_copy[day_int] = shift_int
        shifts_left[shift_int] -= 1
    
    # print("number of -1 :", schedule_copy.count(-1))
    # print("schedule :", schedule_copy)
    return schedule_copy

def evaluate_workload(problem: Problem, staff: Staff, schedule: PersonnalSchedule) -> bool:
    """Returns True if constraint is respected."""

    min_time = staff.min_worktime
    max_time = staff.max_worktime
    time = 0
    for shift_int in [x for x in schedule if x != None]:
        time += problem.shift_types[shift_int].duration
    
    return min_time <= time <= max_time

def evaluate_weekend(staff: Staff, schedule: PersonnalSchedule) -> bool:
    """Returns True if constraint is respected."""

    max_worked_weekends = staff.max_worked_weekends

    weekends = []
    for i in range(len(schedule)//7):
        weekends.append((schedule[7*i+5], schedule[7*i+6]))
    
    for weekend in weekends:
        if weekend[0] != None or weekend[1] != None:
            max_worked_weekends -= 1
    
    return max_worked_weekends >= 0


if __name__ == "__main__":

    problem: Problem = Importer().import_problem("Instance2.txt")
    # sol: Solution = Solution(problem)
    # print(sol.planning)


    a = Solution.from_problem(problem)
    # a.greedy_initialize(problem)
    print(a.planning)
    print("FEASIBLE :", a.is_feasible())

    # test = [-1, None,-1, -1, None, None, None, -1, -1, -1, -1, -1, -1, -1, None, -1, -1, None, -1, -1, None, None, -1]
    # test = [(None if random() > 0.9 else -1) for _ in range(365)]

    # print(test)
    # assign_work_days(problem.staff[0], test)