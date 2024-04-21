import datetime as dt
import os


class Student:
    def __init__(
        self,
        student_id: str,
        student_name: str,
        gender: str,
        dob: str,
    ):
        self.student_id = student_id
        self.student_name = student_name
        self.gender = gender
        self.dob = dt.datetime.strptime(dob, "%Y-%m-%d")
        self.secret_key = os.urandom(16)
        print(f"Secret Key for {self.student_name}: {self.secret_key}")

    def __str__(self) -> str:
        return f"{self.student_name} is a {self.gender} student born on {self.dob} with ID {self.student_id}"


if __name__ == "__main__":
    student = Student(
        "2021A7PS0205H",
        "Arunachala",
        "male",
        "2003-06-24",
    )

    print(student)
