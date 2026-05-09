
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import bcrypt
from db.engine import engine

def add_user(username:str, password:str):
    """
    Creates a new user in the database.

    Validates username and password before insertion:
    - Username must be 3–20 characters long
    - Password must be 8–30 characters long

    Raises:
        ValueError: If username or password does not meet validation rules.
        ValueError: If the username already exists in the database.

    Returns:
        None
    """    
    if not _valid_username(username):
        raise ValueError("Username must be between 3 and 20 characters")
    if not _valid_password(password):
        raise ValueError("Password must be between 8 and 30 characters")
    
    passhash = _hash_password(password)

    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO Users (username, passhash) VALUES (:username, :passhash)"),
                {"username":username, "passhash":passhash}
                )
            conn.commit()
    except IntegrityError:
        raise ValueError("Username already in use")
    
def authenticate_user(username:str, password:str): 
    """
    Returns:
        User_id if credentials are valid, None otherwise.
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, passhash FROM Users WHERE username = :username"),
            {"username": username}
        ).fetchone()

        if result is None:
            return None # username not found
    
        if _verify_password(password, result[1]):
            return result[0]
        else:
            return None # incorrect password
            
def userlist():
    """
    Retrieves all usernames from the Users table.

    Returns:
        list[str]: A list of all usernames in the database.
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT username FROM Users"))
        return [row[0] for row in result.fetchall()]


#--------- User validation methods ---------#

def _valid_username(username):
    return len(username) >= 3 and len(username) <= 20

def _valid_password(password):
    return len(password) >= 8 and len(password) <= 30

#--------- Password hashing and verifying methods ---------#

def _hash_password(password: str):
    """
    Hash a plaintext password using bcrypt.
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

def _verify_password(password: str, hashed: str):
    """
    Verify a plaintext password against a stored hash.

    Returns:
        bool: True if password matches, False otherwise.
    """
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False
