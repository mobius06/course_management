import hashlib
import secrets

def hash_password(password):
    """Hash a password using SHA-256 with a random salt"""
    salt = secrets.token_hex(16)
    # Ensure password is encoded as UTF-8
    password_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    # Combine password and salt
    combined = password_bytes + salt_bytes
    # Generate hash
    hashed = hashlib.sha256(combined).hexdigest()
    return f"{salt}${hashed}"

def verify_password(stored_password, provided_password):
    """Verify a password against its hash"""
    try:
        salt, hashed = stored_password.split('$')
        # Ensure password is encoded as UTF-8
        password_bytes = provided_password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        # Combine password and salt
        combined = password_bytes + salt_bytes
        # Generate hash
        expected = hashlib.sha256(combined).hexdigest()
        return hashed == expected
    except Exception as e:
        print(f"Error in verify_password: {str(e)}")
        return False

# Generate a hash for 'password123'
password = 'password123'
hashed = hash_password(password)
print(f"Generated hash for '{password}': {hashed}")

# Test verification
is_valid = verify_password(hashed, password)
print(f"Verification test result: {is_valid}")

# Test with wrong password
is_valid = verify_password(hashed, 'wrong_password')
print(f"Wrong password test result: {is_valid}") 