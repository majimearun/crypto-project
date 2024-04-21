from cryptography.hazmat.primitives import hashes, hmac
import json
import hashlib
import datetime as dt
from authenticator import ChallengeResponseAuthenticator
class Transaction:
    def __init__(self, university_id: str, student_id: str, code: str, grade: int):
        self.university_id = university_id
        self.student_id = student_id
        self.code = code
        self.grade = grade

    def __str__(self) -> str:
        return f"{self.student_id} received {self.grade} in {self.code} from {self.university_id}"

    def to_dict(self) -> dict:
        return self.__dict__

    def to_bytes(self) -> bytes:
        return json.dumps(self.to_dict(), sort_keys=True).encode()


class Block:
    def __init__(
        self,
        index: int,
        transactions: list[Transaction],
        timestamp: str,
        previous_hash: str,
        nonce: int = 0,
    ):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> bytes:
        in_dict = self.__dict__.copy()
        if in_dict.get("hash"):
            in_dict.pop("hash")
        return hashlib.sha256(json.dumps(in_dict, sort_keys=True).encode()).hexdigest()

    def __str__(self) -> str:
        return f"Block {self.index}\nTimestamp: {self.timestamp}\nPrevious Hash: {self.previous_hash}\nHash: {self.hash}\nNonce: {self.nonce}\nTransactions: {self.transactions}"


class Blockchain:
    def __init__(self, difficulty: int, ledger: dict = None):
        self.chain: list[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.temp_transactions: list[Transaction] = []
        self.ledger = ledger

    def last_block(self) -> Block:
        return self.chain[-1]

    def create_genesis_block(self) -> Block:
        genesis_block = Block(0, [], str(dt.datetime.now()), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def proof_of_work(self, block: Block) -> bytes:
        computed_hash = block.calculate_hash()
        while computed_hash[: self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            computed_hash = block.calculate_hash()
        return computed_hash

    def is_valid_proof(self, block: Block, proof: bytes) -> bool:
        return (
            proof[: self.difficulty] == "0" * self.difficulty
            and proof == block.calculate_hash()
        )

    def add_block(self, block: Block, proof: bytes) -> bool:
        previous_hash = self.last_block().hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def logical_transaction_check(self, transaction: Transaction) -> bool:
        for uni in self.ledger["university"]:
            if uni.university_id == transaction.university_id:
                for cour in uni.courses:
                    if cour.code == transaction.code:
                        break
                else:
                    print("Course not found")
                    return False
                for stud in uni.students:
                    if stud.student_id == transaction.student_id:
                        break
                else:
                    print("Student not found")
                    return False
                break
        else:
            print("University not found")
            return False
        if transaction.grade < 0 or transaction.grade > 10:
            return False
        return True

    def verify_transaction_hmac(self, transaction: Transaction, original_hmac) -> bool:
        uni_id = transaction.university_id
        secret_key = None
        for university in self.ledger["university"]:
            if university.university_id == uni_id:
                secret_key = university.secret_key
                break
        auth = ChallengeResponseAuthenticator(secret_key)
        if auth.authenticate(True):
            in_bytes = transaction.to_bytes()
            HMAC = hmac.HMAC(secret_key, hashes.SHA256())
            HMAC.update(in_bytes)
            try:
                HMAC.verify(original_hmac)
                return True
            except:
                print("Invalid Signature")
                return False

    def add_transaction(self, transaction: Transaction, signature: bytes) -> bool:
        verification = self.verify_transaction_hmac(
            transaction, signature
        ) and self.logical_transaction_check(transaction)
        if not verification:
            return False
        self.temp_transactions.append(transaction.to_dict())
        return True

    def mine(self) -> bool:
        if not self.temp_transactions:
            return False
        last_block = self.last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.temp_transactions,
            timestamp=str(dt.datetime.now()),
            previous_hash=last_block.hash,
        )
        proof = self.proof_of_work(new_block)
        if self.add_block(new_block, proof):
            self.announce_new_block(new_block)
            self.temp_transactions = []
            return True
        else:
            print("Error Mining Block")
            return False

    def announce_new_block(self, block: Block, print_block: bool = False) -> None:
        if self.is_valid_proof(block, block.hash):
            print("New Block Found")
            if print_block:
                print(block)
        return

    def is_chain_valid(self) -> bool:
        previous_hash = self.chain[0].hash
        for block in self.chain[1:]:
            if block.previous_hash != previous_hash:
                return False

            if not self.is_valid_proof(block, block.hash):
                return False

            previous_hash = block.hash
        return True

    def view_student_transcript(
        self, university_id: str, student_id: str
    ) -> tuple[bool, dict]:
        if not self.is_chain_valid():
            return False, {}, 0
        student_transcript = {}
        for block in self.chain:
            for transaction in block.transactions:
                transaction = Transaction(**transaction)
                if (
                    transaction.student_id == student_id
                    and transaction.university_id == university_id
                ):
                    student_transcript[transaction.code] = transaction.grade
                    
        ncreds = 0
        value = 0
        for university in self.ledger["university"]:
            if university.university_id == university_id:
                break
        for course_code in student_transcript:
            for course in university.courses:
                if course.code == course_code:
                    ncreds += course.credits
                    value += course.credits * student_transcript[course_code]
                    break
        return True, student_transcript, value / ncreds


if __name__ == "__main__":
    import university
    import student
    import course
    uni = university.University("BITS", "BITS Pilani")
    student1 = student.Student("2021A7PS0205H", "Arun", "male", "2003-06-24")
    uni.add_student(student1)
    course1 = course.Course("Blockchain", "CS101", 4)
    uni.add_course(course1)
    key = uni.secret_key
    blockchain = Blockchain(2, {"university": [uni], "student": [], "course": []})
    transaction = Transaction("BITS", "2021A7PS0205H", "CS101", 10)
    HMAC = hmac.HMAC(key, hashes.SHA256())
    HMAC.update(transaction.to_bytes())
    signature = HMAC.finalize()

    # will print invalid signature
    if blockchain.add_transaction(transaction, b"wrong_signature"):
        blockchain.mine()
    else:
        print("Transaction failed")

    if blockchain.add_transaction(transaction, signature):
        blockchain.mine()
    else:
        print("Transaction failed")

    print(blockchain.view_student_transcript("BITS", "2021A7PS0205H")[1])
