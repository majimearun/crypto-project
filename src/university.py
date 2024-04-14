import datetime as dt
import student

class University:
    def __init__(self, uni_name, uni_id):
        self.name = uni_name
        self.id = uni_id
        self.students = {}
        self.courses_offered = {}
        
    def add_student(self, student: student.Student):
        # check if the courses are offered by the university
        for course in student.courses:
            if course not in self.courses_offered:
                raise Exception(f"Course {course} is not offered by the university")
        self.students[student.studentID] = student
    
    def add_course(self, course_id, course_name):
        self.courses_offered[course_id] = course_name
    
    def get_course(self, course_id):
        return self.courses_offered.get(course_id, None)
    
    def get_student(self, student_id):
        return self.students.get(student_id, None)