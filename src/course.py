class Course:
    def __init__(self, name, code, credits):
        self.name = name
        self.code = code
        self.credits = credits

    def __str__(self):
        return f"{self.code} : {self.name} - {self.credits} credits"
    
if __name__ == "__main__":
    course = Course("Blockchain", "CS101", 4)
    print(course)
