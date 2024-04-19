import datetime as dt


class Student:
    def __init__(
        self,
        student_id: str,
        student_name: str,
        gender: str,
        age: int,
        dob: str,
    ):
        self.studentID = student_id
        self.studentName = student_name
        self.gender = gender
        self.age = age
        self.dob = dt.datetime.strptime(dob, "%Y-%m-%d")

    def __str__(self) -> str:
        return f"{self.studentName} is a {self.age} year old {self.gender} with ID {self.studentID}"


if __name__ == "__main__":
    student = Student(
        "2021A7PS0205H",
        "Arunachala",
        "Male",
        20,
        "2003-06-24",
    )
    
    print(student)
