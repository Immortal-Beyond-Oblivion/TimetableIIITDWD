# src/models/timetable.py
class Timetable:
    def __init__(self):
        self.assignments = {}  # Maps (course, component, section) to (room, timeslot)
        
    def add_assignment(self, course, component, section, room, timeslot):
        key = (course, component, section)
        self.assignments[key] = (room, timeslot)
    
    def remove_assignment(self, course, component, section):
        key = (course, component, section)
        if key in self.assignments:
            del self.assignments[key]
    
    def get_assignments_for_course(self, course):
        return {key: value for key, value in self.assignments.items() 
                if key[0] == course}
    
    def get_assignments_for_room(self, room):
        return {key: value for key, value in self.assignments.items() 
                if value[0] == room}
    
    def get_assignments_for_instructor(self, instructor):
        return {key: value for key, value in self.assignments.items() 
                if key[0].instructor == instructor}