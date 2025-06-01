import hashlib
import secrets

def hash_password(password):
    """Hash a password using SHA-256 with a random salt"""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

# Generate hash for password123
hashed_password = hash_password("password123")
print(f"Generated hash for 'password123': {hashed_password}")

# Test verification
def verify_password(stored_password, provided_password):
    """Verify a password against its hash"""
    try:
        salt, hashed = stored_password.split('$')
        expected = hashlib.sha256((provided_password + salt).encode()).hexdigest()
        return hashed == expected
    except Exception as e:
        print(f"Error in verify_password: {str(e)}")
        return False

# Test the verification
is_valid = verify_password(hashed_password, "password123")
print(f"Verification test result: {is_valid}") 