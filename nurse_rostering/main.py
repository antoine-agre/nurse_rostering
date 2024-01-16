class Staff:
    
    def __init__(self, min_worktime: int, max_worktime: int, min_consecutive_shifts: int, max_consecutive_shifts: int, min_consecutive_rest_days: int, max_worked_weekends: int):
        
        self.rest_days: list[int] = []
        self.min_worktime: int = min_worktime
        self.max_worktime: int = max_worktime
        self.min_consecutive_shifts: int = min_consecutive_shifts
        self.max_consecutive_shifts: int = max_consecutive_shifts
        self.min_consecutive_rest_days: int = min_consecutive_rest_days
        self.max_worked_weekends: int = max_worked_weekends
        # Pour chaque poste, le nombre de jour maximum où cet employé peut y être assigné
        self.max_shift_days: list[int] = []
        # Pour chaque jour et poste, la pénalité si l'employé ni est pas assigné
        self.shift_wish_penalties: list[list[int]] = []
        # Pour chaque jour et poste, la pénalité si l'employé y est assigné
        self.shift_avoid_penalties: list[list[int]] = []

class ShiftType:
    
    def __init__(self, duration: int):
        self.duration: int = duration
        self.blocked_shift_types: list[ShiftType] = []
        # Pour chaque jour, représente le nombre d'employés requis.
        self.staff_requirements: list[int] = []
        # Pour chaque jour, pénalité par employé au-dessus du nombre requis
        self.cover_above_penalties: list[int] = []
        # Pour chaque jour, pénalité par employé en-dessous du nombre requis
        self.cover_below_penalties: list[int] = []

class Problem:

    def __init__(self, days_count: int):
        self.days_count: int = days_count
        self.staff: list[Staff] = []
        self.shift_types: list[ShiftType] = []

        self.staff_dict: dict[str, int] = {}
        self.shift_dict: dict[str, int] = {}

# Exemple basé sur l'instance 1
problem: Problem = Problem(14)
problem.shift_types.append(ShiftType(480))
staff = Staff(max_worktime=4320, min_worktime=3360, max_consecutive_shifts=5, min_consecutive_shifts=2, min_consecutive_rest_days=2, max_worked_weekends=1)
staff.max_shift_days = [14]
problem.staff.append(staff)