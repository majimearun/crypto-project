from cryptography.hazmat.primitives import hashes, hmac
import argparse


parser = argparse.ArgumentParser(description="Get the response for the challenge")
parser.add_argument("challenge", type=str, help="The challenge to respond to")
parser.add_argument("secret_key", type=str, help="The secret key to use for HMAC")

args = parser.parse_args()
challenge = eval(args.challenge)
secret_key = eval(args.secret_key)

HMAC = hmac.HMAC(secret_key, hashes.SHA256())
HMAC.update(challenge)

print(HMAC.finalize())
