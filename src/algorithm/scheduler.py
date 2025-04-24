# src/algorithm/scheduler.py
import random
from datetime import datetime, timedelta
from src.models.time_slot import TimeSlot
from src.models.timetable import Timetable

class SchedulingAlgorithm:
    def __init__(self, courses, rooms, constraint_engine, student_registrations=None):
        self.courses = courses
        self.rooms = rooms
        self.constraint_engine = constraint_engine
        self.student_registrations = student_registrations or {}
        self.working_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.working_hours = {
            "start": datetime.strptime("09:00", "%H:%M").time(),
            "end": datetime.strptime("18:00", "%H:%M").time()
        }
        self.breaks = {
            "morning": {"start": "10:30", "end": "10:45"},
            "lunch": {"start": "12:30", "end": "14:30"},
            "afternoon": {"start": "15:30", "end": "15:35"}
        }
    # In SchedulingAlgorithm.generate_timetable
    def generate_timetable(self):
        timetable = Timetable()
        
        # Sort courses by complexity (number of components, number of students)
        sorted_courses = sorted(self.courses, 
                            key=lambda c: (sum(c.ltps_structure.values()), c.registered_students),
                            reverse=True)
        
        print(f"Attempting to schedule {len(sorted_courses)} courses")
        
        success_count = 0
        failure_count = 0
        
        for course in sorted_courses:
            print(f"\nProcessing course {course.code}")
            print(f"LTPS structure: {course.ltps_structure}")
            
            for component, hours in course.ltps_structure.items():
                if hours == 0:  # Skip components with zero hours
                    print(f"Skipping {component} (0 hours)")
                    continue
                    
                print(f"Scheduling {component} component ({hours} hours)")
                for section in range(course.sections):
                    result = self._schedule_component(timetable, course, component, section, hours)
                    if result:
                        success_count += 1
                    else:
                        failure_count += 1
        
        print(f"Scheduling completed. Successes: {success_count}, Failures: {failure_count}")
        return timetable
    
    def _schedule_component(self, timetable, course, component, section, hours):
        # Find suitable room and time slot
        suitable_rooms = self._get_suitable_rooms(course, component)
        print(f"Found {len(suitable_rooms)} suitable rooms")
    
        if not suitable_rooms:
            print(f"ERROR: No suitable rooms for {course.code} {component}")
            return False
        # Shuffle rooms to avoid biased assignments
        random.shuffle(suitable_rooms)
        
        for room in suitable_rooms:
            possible_timeslots = self._generate_possible_timeslots(component, hours)
            print(f"Generated {len(possible_timeslots)} possible timeslots")
        
            if not possible_timeslots:
                print(f"ERROR: No possible timeslots for {course.code} {component}")
                continue

            random.shuffle(possible_timeslots)
            
            for timeslot in possible_timeslots:
                if self.constraint_engine.is_valid_assignment(
                        timetable, course, component, section, room, timeslot):
                    print(f"SUCCESS: Added {course.code} {component} to {room.name} at {timeslot.day} {timeslot.start_time}-{timeslot.end_time}")
                    timetable.add_assignment(course, component, section, room, timeslot)
                    return True
                    
        # If we couldn't find a valid assignment, return False
        return False
    
    def _get_suitable_rooms(self, course, component):
        # Find rooms suitable for this course component
        suitable_rooms = []
        for room in self.rooms:
            # For lab components, we need lab rooms
            if component == 'P' and not room.is_lab:
                continue
            # Room should have enough capacity
            if room.capacity < course.registered_students / course.sections:
                continue
            suitable_rooms.append(room)
        return suitable_rooms
    
    # src/algorithm/scheduler.py (update time slot generation)
    def _generate_possible_timeslots(self, component, hours):
        # Duration based on component type
        if component == 'L' or component == 'T':
            duration_minutes = 60  # Fixed 1-hour slots
            increment = 60  # No overlapping slots
        elif component == 'P':
            duration_minutes = 120  # Fixed 2-hour slots
            increment = 120  # No overlapping slots
        elif component == 'S':
            return []  # Self-study doesn't need scheduling
        else:
            raise ValueError(f"Unknown component type: {component}")

        
        timeslots = []
        for day in self.working_days:
            current_time = datetime.combine(datetime.today(), self.working_hours["start"])
            end_time = datetime.combine(datetime.today(), self.working_hours["end"])
            
            while current_time + timedelta(minutes=duration_minutes) <= end_time:
                # Check breaks
                is_break_time = False
                for break_name, break_time in self.breaks.items():
                    break_start = datetime.strptime(break_time["start"], "%H:%M").time()
                    break_end = datetime.strptime(break_time["end"], "%H:%M").time()
                    
                    slot_end = current_time + timedelta(minutes=duration_minutes)
                    if not (slot_end.time() <= break_start or current_time.time() >= break_end):
                        is_break_time = True
                        break
                
                if not is_break_time:
                    timeslots.append(TimeSlot(
                        day=day,
                        start_time=current_time.time(),
                        end_time=(current_time + timedelta(minutes=duration_minutes)).time()
                    ))
                
                # Move to next non-overlapping slot
                current_time += timedelta(minutes=increment)
        
        return timeslots