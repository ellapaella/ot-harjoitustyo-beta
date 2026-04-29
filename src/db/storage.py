
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from db.engine import engine

def add_user(username, password):
    """
    Creates a new user in the database.

    Validates username and password before insertion:
    - Username must be 3–20 characters long
    - Password must be 8–30 characters long

    Args:
        username (str): The username to create.
        password (str): The user's password (stored as hash).

    Raises:
        ValueError: If username or password does not meet validation rules.
        IntegrityError: If the username already exists in the database.

    Returns:
        None
    """    
    if not _valid_username(username):
        raise ValueError("Username must be between 3 and 20 characters")
    if not _valid_password(password):
        raise ValueError("Password must be between 8 and 30 characters")
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO Users (username, passhash) VALUES (:username, :passhash)"),
                {"username":username, "passhash":password}
                )
            conn.commit()
    except IntegrityError:
        raise ValueError("Username already in use")
            
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
