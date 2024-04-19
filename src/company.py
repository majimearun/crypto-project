class Company:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Company: {self.name}"


if __name__ == "__main__":
    company = Company("Adobe")
    print(company)
