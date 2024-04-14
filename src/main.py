from blockchain import Blockchain
from explorer import BlockchainExplorer
from student import Student
from transcript import Transcript
import datetime as dt
from cryptography.fernet import Fernet

print("Creating a new Student Bob")
bob = Student(
    "2021A7PS0001H",
    "Bob",
    2021,
    "M",
    20,
    dt.date(2001, 1, 1),
    {"CS101": "A", "CS102": "B"},
)

print("Creating a new Student Alice")
alice = Student(
    "2021A7PS0002H",
    "Alice",
    2021,
    "F",
    20,
    dt.date(2001, 1, 1),
    {"CS101": "A", "CS102": "B"},
)

print("\nCreating a new Blockchain")
blockchain = Blockchain()
explorer = BlockchainExplorer(blockchain)

print("")
print("Adding blocks to the blockchain: We first add bob's transcript")
blockchain.add_block(
    Transcript(
        bob.studentID,
        Fernet(bob.encryption_key).encrypt(str(bob.courses).encode()),
        "0",
    )
)
print("Adding blocks to the blockchain: We then add alice's transcript")
blockchain.add_block(
    Transcript(
        alice.studentID,
        Fernet(alice.encryption_key).encrypt(str(alice.courses).encode()),
        "0",
    )
)

print("Verifying the blockchain: ", explorer.verify_blockchain())

print("")
print("Getting the block data for Bob")
print(explorer.get_block(1, bob.encryption_key).data)

print("Attempting to get the block data for Bob with Alice's encryption key")
print(explorer.get_block(1, alice.encryption_key).data)
