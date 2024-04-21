import os


class Company:
    def __init__(self, name):
        self.name = name
        self.secret_key = os.urandom(16)
        print(f"Secret Key for {self.name}: {self.secret_key}")

    def __str__(self):
        return f"Company: {self.name}"


if __name__ == "__main__":
    company = Company("Adobe")
    print(company)
