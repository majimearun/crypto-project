import authenticator
import blockchain
from seed import Data
from cryptography.hazmat.primitives import hashes, hmac
import random
from student import Student
from course import Course
from company import Company
from university import University
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--difficulty", type=int, default=2)
parser.add_argument("--testing", type=bool, default=False)
parser.add_argument("--rounds", type=int, default=1)
args = parser.parse_args()

N_ROUNDS = args.rounds
DIFFICULTY = args.difficulty
TESTING = args.testing

# create some transactions in the block chain
data = Data()
ledger = {
    "university": data.university_ledger,
    "student": data.student_ledger,
    "course": data.course_ledger,
    "company": data.company_ledger,
}

BLOCKCHAIN = blockchain.Blockchain(DIFFICULTY, ledger)


for i in range(1, 101):
    uni = random.choice(BLOCKCHAIN.ledger["university"])
    stud = random.choice(BLOCKCHAIN.ledger["student"])
    cour = random.choice(BLOCKCHAIN.ledger["course"])
    grade = random.randint(1, 10)
    transaction = blockchain.Transaction(
        uni.university_id, stud.student_id, cour.code, grade
    )
    HMAC = hmac.HMAC(uni.secret_key, hashes.SHA256())
    HMAC.update(transaction.to_bytes())
    signature = HMAC.finalize()
    BLOCKCHAIN.add_transaction(transaction, signature, True)

    if i % 10 == 0:
        BLOCKCHAIN.mine()


def university_login():
    print("----------------------------------------------------------")
    print("---------------------University Login---------------------")
    print("----------------------------------------------------------")
    name = input("Enter university name: ")
    flag = False
    for uni in BLOCKCHAIN.ledger["university"]:
        if uni.university_name == name:
            flag = True
            break
    if not flag:
        print("University not found")
        return

    auth = authenticator.ChallengeResponseAuthenticator(uni.secret_key, N_ROUNDS)
    if auth.authenticate(TESTING):
        print("Authenticated...")
        print("Access granted")
        print(f"Welcome {name}")
        while True:
            print("----------------------------------------------------------")
            print("1. Add Student")
            print("2. Add Course")
            print("3. Create new entry")
            print("4. View student transcript")
            print("5. View all grades in university")
            print("6. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    student_id = input("Enter student id: ")
                    while True:
                        for stud in uni.students:
                            if stud.student_id == student_id:
                                print("Student already exists")
                                break
                        else:
                            break
                        student_id = input("Enter student id: ")
                    name = input("Enter student name: ")
                    gender = input("Enter gender of student: ")
                    dob = input("Enter date of birth of student (yyyy-mm-dd): ")
                    try:
                        stud = Student(student_id, name, gender, dob)
                    except:
                        print("Invalid date of birth")
                        continue
                    uni.add_student(stud)
                    BLOCKCHAIN.ledger["student"].append(stud)
                    print("Student added successfully:")
                    print(stud)
                case "2":
                    course_code = input("Enter course code: ")
                    while True:
                        for cour in uni.courses:
                            if cour.code == course_code:
                                print("Course already exists")
                                break
                        else:
                            break
                        course_code = input("Enter course code: ")
                    name = input("Enter course name: ")
                    credits = int(input("Enter credits of course: "))
                    cour = Course(course_code, name, credits)
                    uni.add_course(cour)
                    BLOCKCHAIN.ledger["course"].append(cour)
                    print("Course added successfully:")
                    print(cour)
                case "3":
                    while True:
                        student_id = input("Enter student id: ")
                        if any(stud.student_id == student_id for stud in uni.students):
                            break
                    while True:
                        course_code = input("Enter course code: ")
                        if any(course.code == course_code for course in uni.courses):
                            break
                    grade = int(input("Enter grade: "))
                    transaction = blockchain.Transaction(
                        uni.university_id, student_id, course_code, grade
                    )
                    HMAC = hmac.HMAC(uni.secret_key, hashes.SHA256())
                    HMAC.update(transaction.to_bytes())
                    signature = HMAC.finalize()
                    if BLOCKCHAIN.add_transaction(transaction, signature):
                        print("Transaction added successfully")
                    else:
                        print("Transaction failed")
                    if len(BLOCKCHAIN.temp_transactions) == 10:
                        BLOCKCHAIN.mine()
                case "4":
                    student_id = input("Enter student id: ")
                    found, transcript, cgpa = BLOCKCHAIN.view_student_transcript(
                        uni.university_id, student_id
                    )
                    if found:
                        json_transcript = json.dumps(transcript, indent=4)
                        print(f"CGPA: {cgpa}")
                        print(json_transcript)
                    else:
                        print("Student has no courses")
                case "5":
                    found, uni_grades = BLOCKCHAIN.view_uni_grades(uni.university_id)
                    if found:
                        print("Grades:")
                        for student_id, course_code, grade in uni_grades:
                            print(f"{student_id} {course_code} {grade}")
                    else:
                        print("No grades found")
                case "6":
                    return
                case _:
                    print("Invalid choice")


def company_login():
    print("----------------------------------------------------------")
    print("----------------------Company Login-----------------------")
    print("----------------------------------------------------------")
    name = input("Enter company name: ")
    flag = False
    for comp in BLOCKCHAIN.ledger["company"]:
        if comp.name == name:
            flag = True
            break
    if not flag:
        print("Company not found")
        return
    auth = authenticator.ChallengeResponseAuthenticator(comp.secret_key, N_ROUNDS)
    if auth.authenticate(TESTING):
        print("Authenticated...")
        print("Access granted")
        print(f"Welcome {name}")
        while True:
            print("----------------------------------------------------------")
            print("1. View Student Transcript")
            print("2. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    university_id = input("Enter university id: ")
                    student_id = input("Enter student id: ")
                    found, transcript, cgpa = BLOCKCHAIN.view_student_transcript(
                        university_id, student_id
                    )
                    if found:
                        json_transcript = json.dumps(transcript, indent=4)
                        print(f"CGPA: {cgpa}")
                        print(json_transcript)
                    else:
                        print(
                            "Error viewing transcript, either student or university not found"
                        )
                case "2":
                    return
                case _:
                    print("Invalid choice")


def student_login():
    print("----------------------------------------------------------")
    print("----------------------Student Login-----------------------")
    print("----------------------------------------------------------")
    university_name = input("Enter university name: ")
    student_id = input("Enter student id: ")
    flag = False
    for uni in BLOCKCHAIN.ledger["university"]:
        if uni.university_name == university_name:
            flag = True
            break
    if not flag:
        print("University not found")
        return
    flag = False
    for stud in uni.students:
        if stud.student_id == student_id:
            flag = True
            break
    if not flag:
        print("Student not found")
        return
    print(stud.secret_key)
    auth = authenticator.ChallengeResponseAuthenticator(stud.secret_key, N_ROUNDS)
    if auth.authenticate(TESTING):
        print("Authenticated...")
        print("Access granted")
        print(f"Welcome {student_id}")
        while True:
            print("----------------------------------------------------------")
            print("1. View Transcript")
            print("2. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    found, transcript, cgpa = BLOCKCHAIN.view_student_transcript(
                        uni.university_id, student_id
                    )
                    if found:
                        json_transcript = json.dumps(transcript, indent=4)
                        print(f"CGPA: {cgpa}")
                        print(json_transcript)
                    else:
                        print(
                            "Error viewing transcript, either student or university not found"
                        )
                case "2":
                    return
                case _:
                    print("Invalid choice")


def new_user():
    print("----------------------------------------------------------")
    print("----------------------New User Login----------------------")
    print("----------------------------------------------------------")
    print("Select type of user")
    print("1. University")
    print("2. Company")
    choice = input("Enter choice: ")
    match choice:
        case "1":
            university_id = input("Enter university id: ")
            if any(
                uni.university_id == university_id
                for uni in BLOCKCHAIN.ledger["university"]
            ):
                print("University already exists")
                return
            name = input("Enter university name: ")
            if any(
                uni.university_name == name for uni in BLOCKCHAIN.ledger["university"]
            ):
                print("University already exists")
                return
            uni = University(university_id, name)
            BLOCKCHAIN.ledger["university"].append(uni)
            print("University added successfully")
        case "2":
            name = input("Enter company name: ")
            if any(comp.name == name for comp in BLOCKCHAIN.ledger["company"]):
                print("Company already exists")
                return
            comp = Company(name)
            BLOCKCHAIN.ledger["company"].append(comp)
            print("Company added successfully")
        case _:
            print("Invalid choice")


if __name__ == "__main__":
    while True:
        print(
            "Login as ...\n0. New user\n1. University\n2. Student\n3. Company\n4. Exit"
        )
        choice = input("Enter choice: ")
        match choice:
            case "0":
                new_user()
            case "1":
                university_login()
            case "2":
                student_login()
            case "3":
                company_login()
            case "4":
                break
            case _:
                print("Invalid choice")
