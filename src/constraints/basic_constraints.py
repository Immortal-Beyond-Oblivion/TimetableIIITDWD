# src/constraints/basic_constraints.py
# src/constraints/basic_constraints.py
def no_room_conflict(timetable, course, component, section, room, timeslot):
    """
    REQ-01: Ensure no two courses are scheduled in the same room at overlapping times
    """
    for (_, _, _), (r, ts) in timetable.assignments.items():
        if r == room and ts.overlaps(timeslot):
            return False
    return True

def no_instructor_conflict(timetable, course, component, section, room, timeslot):
    """
    REQ-01: Ensure no instructor is teaching two courses at overlapping times
    """
    current_faculty = course.faculty_ids
    for (c, _, _), (_, ts) in timetable.assignments.items():
        if any(faculty_id in c.faculty_ids for faculty_id in current_faculty) and ts.overlaps(timeslot):
            return False
    return True

def no_student_conflict(timetable, course, component, section, room, timeslot, student_registrations):
    """
    REQ-01: Ensure no student is scheduled for two courses at overlapping times
    """
    students_in_course = [
        sid for sid, codes in student_registrations.items() 
        if course.code in codes
    ]
    
    for (c, _, _), (_, ts) in timetable.assignments.items():
        if ts.overlaps(timeslot):
            students_in_other_course = [
                sid for sid, codes in student_registrations.items() 
                if c.code in codes
            ]
            if any(sid in students_in_other_course for sid in students_in_course):
                return False
    return True

def ltps_structure_compliance(timetable, course, component, section, room, timeslot):
    """
    REQ-06: Ensure the LTPS structure is respected
    """
    required_duration = 0
    if component == 'L':  # Lecture
        required_duration = 60  # 1 hour or 60 minutes
    elif component == 'T':  # Tutorial
        required_duration = 60  # 1 hour or 60 minutes
    elif component == 'P':  # Practical
        required_duration = 120  # 2 hours or 120 minutes
    elif component == 'S':  # Self-study - This might not need scheduling
        return True  # Skip checking for self-study
    
    return timeslot.duration_minutes() >= required_duration

def lab_room_requirement(timetable, course, component, section, room, timeslot):
    """
    REQ-08: Ensure lab components are scheduled in lab rooms
    """
    if component == 'P' and not room.is_lab:
        return False
    return True

def room_capacity_check(timetable, course, component, section, room, timeslot):
    students_per_section = course.registered_students / course.sections
    return room.capacity >= students_per_section