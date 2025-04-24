# src/models/course.py
class Course:
    def __init__(self, course_id, department, semester, course_code, course_name, 
                 L, T, P, S, C, semester_type, faculty_ids, combined, capacity):
        self.id = course_id
        self.department = department
        self.semester = semester  # Now a string like "2A_premid"
        self.code = course_code
        self.name = course_name
        self.ltps_structure = {'L': L, 'T': T, 'P': P, 'S': S}  # Built from columns
        self.credits = C
        self.faculty_ids = faculty_ids  # List of faculty IDs
        self.combined = combined == "TRUE"
        self.registered_students = capacity  # Capacity = registered_students
        self.sections = self._calculate_sections()
        self.lab_required = P > 0  # Determine lab need from P hours

    def _calculate_sections(self):
        # REQ-03: Calculate sections based on capacity
        if self.registered_students > 100:
            return max(1, self.registered_students // 100)
        return 1