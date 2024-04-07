import datetime as dt
from cryptography.fernet import Fernet


class Student:
    def __init__(
        self,
        studentID: str,
        studentName: str,
        yearOfJoining: int,
        gender: str,
        age: int,
        dob: dt.date,
        courses: dict[str, str] = {},
    ):
        self.studentID = studentID
        self.studentName = studentName
        self.yearOfJoining = yearOfJoining
        self.gender = gender
        self.age = age
        self.dob = dob
        self.courses = {course: grade for course, grade in courses.items()}
        self.encryption_key = Fernet.generate_key()
        


if __name__ == "__main__":
    student = Student(
        "2021A7PS0001H",
        "Alice",
        2021,
        "F",
        20,
        dt.date(2001, 1, 1),
        {"CS101": "A", "CS102": "B"},
    )
    print(student.encryption_key)
        