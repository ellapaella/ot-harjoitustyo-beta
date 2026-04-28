
from sqlalchemy import text
from db.engine import engine

def add_user(username, password):
    
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
    except:
        raise ValueError("Username already in use")
            
def userlist():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT username FROM Users"))
        return [row[0] for row in result.fetchall()]


#--------- User validation methods ---------#

def _valid_username(username):
    return len(username) >= 3 and len(username) <= 20

def _valid_password(password):
    return len(password) >= 8 and len(password) <= 30
