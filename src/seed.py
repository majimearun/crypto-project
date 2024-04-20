import random
import student
import university
import company
import course


class Data:
    def __init__(self):
        uni1 = university.University("1", "IIT Bombay")
        uni2 = university.University("2", "IIT Delhi")
        uni3 = university.University("3", "IIT Madras")
        uni4 = university.University("4", "BITS Pilani")
        uni5 = university.University("5", "BITS Hyderabad")
        self.university_ledger = [uni1, uni2, uni3, uni4, uni5]

        student1 = student.Student("1", "Alice", "female", "2003-06-24")
        student2 = student.Student("2", "Bob", "male", "2003-06-24")
        student3 = student.Student("3", "Charlie", "male", "2003-06-24")
        student4 = student.Student("4", "David", "male", "2003-06-24")
        student5 = student.Student("5", "Eve", "female", "2003-06-24")
        self.student_ledger = [student1, student2, student3, student4, student5]

        company1 = company.Company("Adobe")
        company2 = company.Company("Microsoft")
        company3 = company.Company("Google")
        company4 = company.Company("Facebook")
        company5 = company.Company("Amazon")
        self.company_ledger = [company1, company2, company3, company4, company5]

        course1 = course.Course("1", "Blockchain", 3)
        course2 = course.Course("2", "Cryptography", 4)
        course3 = course.Course("3", "AI", 2)
        course4 = course.Course("4", "ML", 5)
        course5 = course.Course("5", "DL", 2)
        self.course_ledger = [course1, course2, course3, course4, course5]

        for stud in self.student_ledger:
            uni1.add_student(stud)
            uni2.add_student(stud)
            uni3.add_student(stud)
            uni4.add_student(stud)
            uni5.add_student(stud)

        for c in self.course_ledger:
            uni1.add_course(c)
            uni2.add_course(c)
            uni3.add_course(c)
            uni4.add_course(c)
            uni5.add_course(c)
