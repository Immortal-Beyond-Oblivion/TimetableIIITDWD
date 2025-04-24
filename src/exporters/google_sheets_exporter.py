# src/exporters/google_sheets_exporter.py
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

class GoogleSheetsExporter:
    def __init__(self, credentials_file):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
        self.service = build('sheets', 'v4', credentials=self.creds)
        
    def export_timetable(self, timetable, sheet_id):
        semester_dept_pairs = self._extract_semester_dept_pairs(timetable)
        
        for semester, department in semester_dept_pairs:
            self._create_semester_dept_sheet(sheet_id, timetable, semester, department)
            
        return sheet_id
    
    def _extract_semester_dept_pairs(self, timetable):
        pairs = set()
        for (course, _, _) in timetable.assignments.keys():
            # Extract base semester (e.g., "2A_premid" → "2")
            base_semester = ''.join(filter(str.isdigit, course.semester))
            pairs.add((base_semester, course.department))
        return sorted(list(pairs), key=lambda x: (int(x[0]), x[1]))
    
    def _create_semester_dept_sheet(self, sheet_id, timetable, semester, department):
        sheet_name = f"Semester {semester} {department}"
        
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])
        
        sheet_exists = any(sheet.get("properties", {}).get("title") == sheet_name 
                       for sheet in sheets)
        
        if not sheet_exists:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=sheet_id,
                body={'requests': [{'addSheet': {'properties': {'title': sheet_name}}}]}
            ).execute()
        else:
            self.service.spreadsheets().values().clear(
                spreadsheetId=sheet_id,
                range=f"{sheet_name}!A1:Z1000"
            ).execute()
        
        timetable_data = self._generate_semester_dept_data(timetable, semester, department)
        self.service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="USER_ENTERED",
            body={"values": timetable_data}
        ).execute()
    
    def _generate_semester_dept_data(self, timetable, semester, department):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        time_slots = ["9:00-10:00", "10:00-11:00", "11:00-12:00", 
                     "12:00-13:00", "13:00-14:00", "14:00-15:00", 
                     "15:00-16:00", "16:00-17:00", "17:00-18:00"]
        
        data = [["Time Slot"] + days]
        
        for slot in time_slots:
            row = [slot]
            for day in days:
                courses_in_slot = self._find_courses_in_slot(
                    timetable, day, slot, semester, department)
                row.append(courses_in_slot)
            data.append(row)
        
        return data
    
    def _find_courses_in_slot(self, timetable, day, time_slot, semester, department):
        start_time_str, end_time_str = time_slot.split('-')
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()
        
        courses = []
        for (course, component, section), (room, timeslot) in timetable.assignments.items():
            if (course.semester != semester 
                or course.department != department 
                or timeslot.day != day):
                continue
                
            if (timeslot.start_time <= end_time and start_time <= timeslot.end_time):
                course_info = f"{course.code} ({component}{section+1})\n{room.name}"
                courses.append(course_info)
                
        return "\n".join(courses) if courses else ""