class Student:
    def __init__(self, student_id, document, name, surname, email, birthdate):
        self.student_id = student_id # PK
        self.document = document
        self.name = name
        self.surname = surname
        self.email = email
        self.birthdate = birthdate


class Course:
    def __init__(self, course_id, name, description, credits):
        self.course_id = course_id # PK
        self.name = name
        self.description = description
        self.credits = credits


class Enrollement:
    def __init__(self, student_id, course_id, date_enrollment):
        self.student_id = student_id # FK -> estudiante 
        self.course_id = course_id # FK -> curso 
        self.date_enrollment = date_enrollment
                   
