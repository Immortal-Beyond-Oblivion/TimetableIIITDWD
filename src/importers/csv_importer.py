# src/importers/csv_importer.py
import pandas as pd
from src.models.course import Course
from src.models.room import Room

# src/importers/csv_importer.py
class CSVImporter:
    def import_courses(self, file_path):
        df = pd.read_csv(file_path)
        courses = []
        
        for _, row in df.iterrows():
            course = Course(
                course_id=row['COURSE_ID'],
                department=row['DEPARTMENT'],
                semester=row['SEMESTER'],
                course_code=row['COURSE_CODE'],
                course_name=row['COURSE_NAME'],
                L=int(row['L']),
                T=int(row['T']),
                P=int(row['P']),
                S=int(row['S']),
                C=int(row['C']),
                semester_type=row['SEMESTER_TYPE'],
                faculty_ids=self._parse_faculty_ids(row['FACULTY_ID']),
                combined=row['COMBINED'] == "TRUE",
                capacity=int(row['CAPACITY'])
            )
            courses.append(course)
        return courses
    

    def _parse_faculty_ids(self, faculty_str):
        """Handle empty/malformed faculty IDs"""
        if pd.isna(faculty_str) or faculty_str.strip() == "":
            return []
        return [f.strip() for f in str(faculty_str).split(';') if f.strip()]


    def import_rooms(self, file_path):
        df = pd.read_csv(file_path)
        rooms = []
        
        for _, row in df.iterrows():
            # Convert the string value 'True'/'False' to boolean for is_lab
            is_lab = str(row.get('is_lab', "False")).lower() == 'true'
            
            room = Room(
                name=row['room_name'],
                capacity=int(row['capacity']),  # Ensure capacity is an integer
                is_lab=is_lab
            )
            rooms.append(room)
            
        return rooms



    def import_faculty(self, file_path):
        """New method to import faculty data"""
        df = pd.read_csv(file_path)
        return dict(zip(df['FACULTY_ID'], df['NAME']))
    
    
    def import_student_registrations(self, file_path):
        df = pd.read_csv(file_path)
        registrations = {}
        
        # Group by student_id and collect course_codes
        for student_id, group in df.groupby('student_id'):
            registrations[student_id] = group['course_code'].tolist()
            
        return registrations