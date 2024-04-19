import authenticator
import blockchain
import random
import student
import university
import company
import course
from cryptography.hazmat.primitives import hashes, hmac

N_ROUNDS = 1
DIFFICULTY = 4

# create secret key
SECRET_KEY = input("Enter secret key: ").encode()

BLOCKCHAIN = blockchain.Blockchain(DIFFICULTY, SECRET_KEY)

# create university
uni1 = university.University("1", "IIT Bombay")
uni2 = university.University("2", "IIT Delhi")
uni3 = university.University("3", "IIT Madras")
uni4 = university.University("4", "BITS Pilani")
uni5 = university.University("5", "BITS Hyderabad")

# create students
student1 = student.Student("1", "Alice", "Female", 20, "2003-06-24")
student2 = student.Student("2", "Bob", "Male", 20, "2003-06-24")
student3 = student.Student("3", "Charlie", "Male", 20, "2003-06-24")
student4 = student.Student("4", "David", "Male", 20, "2003-06-24")
student5 = student.Student("5", "Eve", "Female", 20, "2003-06-24")

student_ledger = [student1, student2, student3, student4, student5]


# create companies
company1 = company.Company("Adobe")
company2 = company.Company("Microsoft")
company3 = company.Company("Google")
company4 = company.Company("Facebook")
company5 = company.Company("Amazon")

company_ledger = [company1, company2, company3, company4, company5]

# create courses
course1 = course.Course("1", "Blockchain", 3)
course2 = course.Course("2", "Cryptography", 4)
course3 = course.Course("3", "AI", 2)
course4 = course.Course("4", "ML", 5)
course5 = course.Course("5", "DL", 2)

course_ledger = [course1, course2, course3, course4, course5]

# seed data
for stud in student_ledger:
    uni1.add_student(stud)
    uni2.add_student(stud)
    uni3.add_student(stud)
    uni4.add_student(stud)
    uni5.add_student(stud)

for c in course_ledger:
    uni1.add_course(c)
    uni2.add_course(c)
    uni3.add_course(c)
    uni4.add_course(c)
    uni5.add_course(c)


# add some transactions
for i in range(10):
    uni = random.choice([uni1, uni2, uni3, uni4, uni5])
    stud = random.choice(student_ledger)
    course = random.choice(course_ledger)
    grade = random.randint(1, 10)
    transaction = blockchain.Transaction(
        uni.university_id, stud.student_id, course.code, grade
    )
    HMAC = hmac.HMAC(SECRET_KEY, hashes.SHA256())
    HMAC.update(transaction.to_bytes())
    signature = HMAC.finalize()
    BLOCKCHAIN.add_transaction(transaction, signature)

    if i % 2 == 0:
        BLOCKCHAIN.mine()


print("Login as ...\n1. University\n2. Student\n3. Company")
choice = input("Enter choice: ")
match choice:
    case "3":
        name = input("enter company name: ")
        flag = False
        for company in company_ledger:
            if company.name == name:
                flag = True
                break
        if not flag:
            print("Company not found")
            exit()
        authenticator = authenticator.ChallengeResponseAuthenticator(
            SECRET_KEY, N_ROUNDS
        )
        if authenticator.authenticate(True):
            print("Authenticated...")
            print("Access granted")
            print(f"Welcome {name}")
            print("1. View Student Transcript")
            print("2. Exit")
            choice = input("Enter choice: ")
            match choice:
                case "1":
                    university_id = input("Enter university id: ")
                    student_id = input("Enter student id: ")
                    print(BLOCKCHAIN.view_student_transcript(university_id, student_id))
                case "2":
                    exit()
