from blockchain import Blockchain
from explorer import BlockchainExplorer
from student import Student
from transcript import Transcript
import datetime as dt
from cryptography.fernet import Fernet

bob = Student(
    "2021A7PS0001H",
    "Bob",
    2021,
    "M",
    20,
    dt.date(2001, 1, 1),
    {"CS101": "A", "CS102": "B"},
)

alice = Student(
    "2021A7PS0002H",
    "Alice",
    2021,
    "F",
    20,
    dt.date(2001, 1, 1),
    {"CS101": "A", "CS102": "B"},
)

blockchain = Blockchain()
explorer = BlockchainExplorer(blockchain)

blockchain.add_block(
    Transcript(
        bob.studentID,
        Fernet(bob.encryption_key).encrypt(str(bob.courses).encode()),
        "0",
    )
)

blockchain.add_block(
    Transcript(
        alice.studentID,
        Fernet(alice.encryption_key).encrypt(str(alice.courses).encode()),
        "0",
    )
)

print(explorer.verify_blockchain())

print(explorer.get_block(1, bob.encryption_key).data)

# will throw error
# print(explorer.get_block(2, bob.encryption_key).data)
