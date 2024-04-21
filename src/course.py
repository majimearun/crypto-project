class Course:
    def __init__(self, code, name, credits):
        self.name = name
        self.code = code
        self.credits = credits

    def __str__(self):
        return f"{self.code} : {self.name} - {self.credits} credits"


if __name__ == "__main__":
    course = Course("CS101", "Blockchain", 4)
    print(course)
