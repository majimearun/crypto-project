import hashlib
import datetime as dt


class Transcript:
    def __init__(self, studentID: str, data: str, previous_hash: str):
        self.studentID = studentID
        self.data = data
        self.timestamp = dt.datetime.now()
        self.hash = self.calculate_hash()
        self.previous_hash = previous_hash

    def calculate_hash(self) -> str:
        return hashlib.sha256(
            str(self.studentID + str(self.data) + str(self.timestamp)).encode()
        ).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        while self.hash[:difficulty] != "0" * difficulty:
            self.timestamp = dt.datetime.now()
            self.hash = self.calculate_hash()
