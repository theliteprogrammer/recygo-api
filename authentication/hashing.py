from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# function that hashes a password
def get_hashed(password):
    return bcrypt_context.hash(password)
