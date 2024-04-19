from cryptography.hazmat.primitives import hashes, hmac
import os
import random

class ChallengeResponseAuthenticator:
    def __init__(self, secret_key: bytes, n_rounds: int = 1):
        self.secret_key = secret_key
        self.n_rounds = n_rounds

    def authenticate(self) -> bool:
        for _ in range(self.n_rounds):
            challenge = input("Enter the challenge: ").encode()
            random_bit = str(0 if random.randint(0, 1) == 0 else 1).encode()
            print(f"Random bit: {random_bit}")
            print(f"Together: {challenge + random_bit}")
            response = input("Enter the response: ")
            response = eval(response)
            HMAC = hmac.HMAC(self.secret_key, hashes.SHA256())
            HMAC.update(challenge + random_bit)
            try:
                HMAC.verify(response)
                print("Authentication successful")
            except:
                print("Authentication failed")
                return False
        return True


if __name__ == "__main__":
    secret_key = os.urandom(1)
    print(f"Secret Key: {secret_key}")
    authenticator = ChallengeResponseAuthenticator(secret_key, 1)
    if authenticator.authenticate():
        print("Authenticated...")
        print("Access granted")
