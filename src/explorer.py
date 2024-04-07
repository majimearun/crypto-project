from transcript import Transcript
from blockchain import Blockchain
import hashlib
import json
from cryptography.fernet import Fernet


class BlockchainExplorer:
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def verify_blockchain(self) -> bool:
        return self.blockchain.is_valid()

    def verify_block(self, block: Transcript) -> bool:
        return (
            block.hash
            == hashlib.sha256(
                str(
                    block.studentID + str(block.courses) + str(block.timestamp)
                ).encode()
            ).hexdigest()
        )

    def get_block(self, index: int, key: bytes):
        block = self.blockchain.chain[index]
        decoded_string = Fernet(key).decrypt(block.data).decode()
        decoded_string = decoded_string.replace("'", '"')
        block.data = json.loads(decoded_string)
        return block
