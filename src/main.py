import authenticator
import blockchain
from seed import Data
from cryptography.hazmat.primitives import hashes, hmac
import random
import student
import course

N_ROUNDS = 1
DIFFICULTY = 4
SECRET_KEY = input("Enter secret key: ").encode()
BLOCKCHAIN = blockchain.Blockchain(DIFFICULTY, SECRET_KEY)

data = Data()

for i in range(100):
    uni = random.choice(data.university_ledger)
    stud = random.choice(data.student_ledger)
    course = random.choice(data.course_ledger)
    grade = random.randint(1, 10)
    transaction = blockchain.Transaction(
        uni.university_id, stud.student_id, course.code, grade
    )
    HMAC = hmac.HMAC(SECRET_KEY, hashes.SHA256())
    HMAC.update(transaction.to_bytes())
    signature = HMAC.finalize()
    BLOCKCHAIN.add_transaction(transaction, signature)

    if i % 10 == 0:
        BLOCKCHAIN.mine()


def university_login():
    name = input("Enter university name: ")
    flag = False
    for university in data.university_ledger:
        if university.university_name == name:
            flag = True
            break
    if not flag:
        print("University not found")
        return

    auth = authenticator.ChallengeResponseAuthenticator(SECRET_KEY, N_ROUNDS)
    if auth.authenticate(True):
        print("Authenticated...")
        print("Access granted")
        print(f"Welcome {name}")
        while True:
            print("1. Add Student")
            print("2. Add Course")
            print("3. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    student_id = input("Enter student id: ")
                    while True:
                        for stud in data.student_ledger:
                            if stud.student_id == student_id:
                                print("Student already exists")
                                break
                        else:
                            break
                        student_id = input("Enter student id: ")
                    name = input("Enter student name: ")
                    gender = input("Enter gender of student: ")
                    dob = input("Enter date of birth of student: ")
                    stud = student.Student(student_id, name, gender, dob)
                    university.add_student(stud)
                    data.student_ledger.append(stud)
                case "2":
                    course_code = input("Enter course code: ")
                    while True:
                        for course in data.course_ledger:
                            if course.code == course_code:
                                print("Course already exists")
                                break
                        else:
                            break
                        course_code = input("Enter course code: ")
                    name = input("Enter course name: ")
                    credits = input("Enter credits of course: ")
                    course = course.Course(course_code, name, credits)
                    university.add_course(course)
                    data.course_ledger.append(course)
                case "3":
                    return
                case _:
                    print("Invalid choice")


def company_login():
    name = input("Enter company name: ")
    flag = False
    for company in data.company_ledger:
        if company.name == name:
            flag = True
            break
    if not flag:
        print("Company not found")
        return
    auth = authenticator.ChallengeResponseAuthenticator(SECRET_KEY, N_ROUNDS)
    if auth.authenticate(True):
        print("Authenticated...")
        print("Access granted")
        print(f"Welcome {name}")
        while True:
            print("1. View Student Transcript")
            print("2. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    university_id = input("Enter university id: ")
                    student_id = input("Enter student id: ")
                    print(BLOCKCHAIN.view_student_transcript(university_id, student_id))
                case "2":
                    return
                case _:
                    print("Invalid choice")


def student_login():
    university_id = input("Enter university id: ")
    student_id = input("Enter student id: ")
    flag = False
    found_university = None
    for university in data.university_ledger:
        if university.university_id == university_id:
            flag = True
            found_university = university
            break
    if not flag:
        print("University not found")
        return
    flag = False
    for student in found_university.students:
        if student.student_id == student_id:
            flag = True
            break
    if not flag:
        print("Student not found")
        return
    auth = authenticator.ChallengeResponseAuthenticator(SECRET_KEY, N_ROUNDS)
    if auth.authenticate(True):
        print("Authenticated...")
        print("Access granted")
        print(f"Welcome {student_id}")
        while True:
            print("1. View Transcript")
            print("2. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    print(BLOCKCHAIN.view_student_transcript(university_id, student_id))
                case "2":
                    return
                case _:
                    print("Invalid choice")


if __name__ == "__main__":
    while True:
        print("Login as ...\n1. University\n2. Student\n3. Company")
        choice = input("Enter choice: ")
        match choice:
            case "1":
                university_login()
            case "2":
                student_login()
            case "3":
                company_login()
            case _:
                print("Invalid choice")
