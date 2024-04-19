import student
import course


class University:
    def __init__(self, id: str, name: str):
        self.universityID = id
        self.universityName = name
        self.students = []
        self.courses = []
        
    def add_student(self, student: student.Student):
        self.students.append(student)
        
    def add_course(self, course: course.Course):
        self.courses.append(course)
        
    def __str__(self) -> str:
        return f"{self.universityName} has {len(self.students)} students and {len(self.courses)} courses."


if __name__ == "__main__":
    uni = University("BITS", "BITS Pilani")
    print(uni)
    student1 = student.Student("2021A7PS0205H", "Arun", "Male", 20, "2003-06-24")
    uni.add_student(student1)   
    student2 = student.Student("2021A7PS0206H", "Arunachala", "Male", 20, "2003-06-24")
    uni.add_student(student2)
    
    course1 = course.Course("Blockchain", "CS101", 4)
    uni.add_course(course1)
    
    print(uni)