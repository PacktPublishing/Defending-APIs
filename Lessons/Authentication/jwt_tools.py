import jwt
import datetime
import time

# Secret key for encoding and decoding the JWT
SECRET_KEY = '9e44b92ae6296307865c1394c1f5aca80862bb30d99a50b40d4b26d7a749a90d'

def encode():
    # Payload data
    payload = {
        'user_id': 123,
        'email': 'user@example.com',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60) # Token expires in one minute
    }

    # Encode the payload to generate JWT
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print("Encoded JWT:", encoded_jwt)
    return encoded_jwt

def decode(input_jwt):
    try:
        # Decode the JWT
        decoded_jwt = jwt.decode(input_jwt, SECRET_KEY, algorithms=['HS256'])
        print("Decoded JWT:", decoded_jwt)
    except jwt.ExpiredSignatureError:
        # Handle expired token
        print("The token has expired.")
    except jwt.InvalidTokenError:
        # Handle invalid token
        print("Invalid token.")

# Entrypoint from command line invocation
if __name__ == "__main__":
    this_jwt = encode()
    decode(this_jwt)
