# src/constraints/constraint_engine.py
class ConstraintEngine:
    def __init__(self):
        self.constraints = []
        
    def add_constraint(self, constraint_func, weight=1.0):
        self.constraints.append((constraint_func, weight))
        
    def is_valid_assignment(self, timetable, course, component, section, room, timeslot):
        for constraint_func, weight in self.constraints:  # Extract constraint_func from the tuple
            constraint_name = constraint_func.__name__ if hasattr(constraint_func, "__name__") else "lambda"
            if not constraint_func(timetable, course, component, section, room, timeslot):  # Call constraint_func
                print(f"❌ Constraint failed: {constraint_name} for {course.code} {component} in {room.name} at {timeslot.day} {timeslot.start_time}")
                return False
        print(f"✅ All constraints passed for {course.code} {component} in {room.name} at {timeslot.day} {timeslot.start_time}")
        return True
    
    def evaluate_timetable(self, timetable):
        # Calculate a score for the timetable based on how well it satisfies all constraints
        score = 0
        for constraint_func, weight in self.constraints:
            constraint_satisfaction = self._evaluate_constraint(timetable, constraint_func)
            score += constraint_satisfaction * weight
        return score
    
    def _evaluate_constraint(self, timetable, constraint_func):
        # Count how many assignments satisfy this constraint
        satisfied = 0
        total = 0
        
        for (course, component, section), (room, timeslot) in timetable.assignments.items():
            total += 1
            if constraint_func(timetable, course, component, section, room, timeslot):
                satisfied += 1
                
        return satisfied / total if total > 0 else 1.0