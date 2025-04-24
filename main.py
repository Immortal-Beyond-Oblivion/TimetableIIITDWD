# main.py
import os
from src.importers.csv_importer import CSVImporter
from src.constraints.constraint_engine import ConstraintEngine
from src.constraints.basic_constraints import (
    no_room_conflict, no_instructor_conflict, no_student_conflict,
    ltps_structure_compliance, lab_room_requirement, room_capacity_check
)
from src.algorithm.scheduler import SchedulingAlgorithm
from src.exporters.google_sheets_exporter import GoogleSheetsExporter

def main():
    # Initialize the data importer
    importer = CSVImporter()
    
    # Import data
    courses = importer.import_courses("data/courses.csv")
    rooms = importer.import_rooms("data/rooms.csv")
    student_registrations = importer.import_student_registrations("data/registrations.csv")
    faculty_mapping = importer.import_faculty("data/faculty.csv")  # New line
    # Add this to main.py after importing the data
    print(f"Loaded {len(courses)} courses")
    for course in courses[:3]:  # Print first few courses
        print(f"Course: {course.code}, Sections: {course.sections}, Students: {course.registered_students}")

    print(f"Loaded {len(rooms)} rooms")
    for room in rooms[:3]:  # Print first few rooms
        print(f"Room: {room.name}, Capacity: {room.capacity}, Is Lab: {room.is_lab}")
        # Initialize the constraint engine
    constraint_engine = ConstraintEngine()
    
    # Add constraints
    constraint_engine.add_constraint(no_room_conflict)
    constraint_engine.add_constraint(no_instructor_conflict)
    constraint_engine.add_constraint(
        lambda timetable, course, component, section, room, timeslot: 
        no_student_conflict(timetable, course, component, section, room, timeslot, student_registrations)
    )
    constraint_engine.add_constraint(ltps_structure_compliance)
    constraint_engine.add_constraint(lab_room_requirement)
    constraint_engine.add_constraint(room_capacity_check)
    
    # Initialize the scheduling algorithm
    scheduler = SchedulingAlgorithm(courses, rooms, constraint_engine, student_registrations)
    
    # Generate the timetable
    timetable = scheduler.generate_timetable()
    
    # Export to Google Sheets
    exporter = GoogleSheetsExporter("config/credentials.json")
    sheet_id = "1WXQLWusdI8oBuvLqAi07V2yVN_WpqCc9ykTJ95nuvfM"  # Replace with your existing Google Sheet ID
    exporter.export_timetable(timetable, sheet_id)
    
    print(f"Timetable has been updated in Google Sheets: https://docs.google.com/spreadsheets/d/{sheet_id}")

if __name__ == "__main__":
    main()