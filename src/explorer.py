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
                str(block.studentID + str(block.data) + str(block.timestamp)).encode()
            ).hexdigest()
        )

    def get_block(self, index: int, key: bytes):
        block = self.blockchain.chain[index]
        if self.verify_block(block) == False:
            print("Block is tampered or an invalid attempt is being made")
            return None
        try:
            decoded_string = Fernet(key).decrypt(block.data).decode()
            decoded_string = decoded_string.replace("'", '"')
            block.data = json.loads(decoded_string)
        except:
            print("wrong key, cannot decrypt data")
        return block
