import pandas as pd

def generate_registrations():
    # Course mapping for each department and semester
    course_mapping = {
        # ------------------- 2nd Semester -------------------
        ('CSE', 2): [
            'CS162', 'CS164', 'CS163', 'CS165', 
            'HS204 / HS153', 'B1', 'B2'
        ],
        ('DSAI', 2): [
            'MA163', 'CS162', 'CS164', 'DS164', 
            'HS161', 'CS163', 'B1(ASD151/HS151/New/New/New/New)', 
            'B2(New/New/New/New)'
        ],
        ('ECE', 2): [
            'MA202', 'CS162', 'CS164', 'HS161', 
            'CS163', 'new', 'B1','B2'
        ],

        # ------------------- 4th Semester -------------------
        ('CSE', 4): [
            'MA202', 'CS206', 'CS204', 'CS301', 
            'CS310', 'HS205'
        ],
        ('DSAI', 4): [
            'MA202', 'HS206', 'CS204', 'DS204', 
            'CS310', 'DS205'
        ],
        ('ECE', 4): [
            'MA208', 'EC205', 'EC310', 'EC204', 
            'HS204', 'HS205'
        ],

        # ------------------- 6th Semester -------------------
        ('CSE', 6): [
            'B1', 'B2', 'B3', 'B4', 'CS307'
        ],
        ('DSAI', 6): [
            'DS309', 'DS306', 'DS307', 'DS308', 
            'DS399', 'HS101', 'B1', 'B2'
        ],
        ('ECE', 6): [
            'EC307', 'B1', 'B2', 'B3', 'B4'
        ],

        # ------------------- 8th Semester -------------------
        ('CSE', 8): [
            'CS801', 'CS802', 'CS803', 'CS804', 'CS805'
        ],
        ('DSAI', 8): [
            'DS801', 'DS802', 'DS803', 'DS804', 'DS805'
        ],
        ('ECE', 8): [
            'EC801', 'EC802', 'EC803', 'EC804', 'EC805'
        ]
    }

    registrations = []

    # Generate students for each semester
    for base_year, semester in [(24, 2), (23, 4), (22, 6), (21, 8)]:
        # Generate CSE students
        for i in range(1, 148 if semester == 2 else 142):
            student_id = f"{base_year}bcs{i:03d}"
            dept = 'CSE'
            for course in course_mapping.get((dept, semester), []):
                registrations.append({'student_id': student_id, 'course_code': course})

        # Generate DSAI students
        max_dsai = 100 if semester == 2 else 141
        for i in range(1, max_dsai + 1):
            student_id = f"{base_year}bds{i:03d}"
            dept = 'DSAI'
            for course in course_mapping.get((dept, semester), []):
                registrations.append({'student_id': student_id, 'course_code': course})

        # Generate ECE students
        max_ece = 100 if semester == 2 else 141
        for i in range(1, max_ece + 1):
            student_id = f"{base_year}bec{i:03d}"
            dept = 'ECE'
            for course in course_mapping.get((dept, semester), []):
                registrations.append({'student_id': student_id, 'course_code': course})

    # Create DataFrame and save
    df = pd.DataFrame(registrations)
    df.to_csv('registrations.csv', index=False)
    print("Generated registrations.csv with", len(df), "entries")

if __name__ == "__main__":
    generate_registrations()