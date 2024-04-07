from transcript import Transcript


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self) -> Transcript:
        return Transcript("0", "Genesis Block", "0")

    def get_latest_block(self) -> Transcript:
        return self.chain[-1]

    def add_block(self, new_block: Transcript, pow_difficulty: int = 2) -> int:
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        new_block.mine_block(pow_difficulty)
        self.chain.append(new_block)
        return len(self.chain) - 1

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True
