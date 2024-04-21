from cryptography.hazmat.primitives import hashes, hmac

challenge = eval(input("Enter the challenge: "))
secret_key = eval(input("Enter the secret key: "))

HMAC = hmac.HMAC(secret_key, hashes.SHA256())
HMAC.update(challenge)

print(HMAC.finalize())
