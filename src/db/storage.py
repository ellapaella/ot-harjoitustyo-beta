
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import bcrypt
import json
from db.engine import engine

def create_user(username:str, password:str):
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
        
def create_plot(owner_id: int, plot_name: str, description: str,
                distribution_type: str, parameters: dict):
    """
    Creates and saves a new plot for a specific user.

    Args:
        owner_id (int): ID of the user creating the plot.
        plot_name (str): Name of the plot.
        description (str): Optional user description of the plot.
        distribution_type (str): Type of probability distribution
            (e.g. normal, binomial, poisson).
        parameters (dict): Distribution parameters stored as JSON.

    Raises:
        ValueError: If plot_name is empty.

    Returns:
        None
    """

    if not plot_name.strip():
        raise ValueError("Plot name cannot be empty")

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO Plots 
                (owner_id, plot_name, description, distribution_type, parameters)
                VALUES
                (:owner_id, :plot_name, :description, :distribution_type, :parameters)
            """),
            {
                "owner_id": owner_id,
                "plot_name": plot_name,
                "description": description,
                "distribution_type": distribution_type,
                "parameters": json.dumps(parameters)
            }
        )
        conn.commit()

def get_user_plots(owner_id: int):
    """
    Retrieves all plots belonging to a specific user.

    Args:
        owner_id (int): ID of the plot owner.

    Returns:
        list: A list of database rows containing:
            - plot id
            - plot name
            - description
            - distribution type
            - parameters

    Notes:
        Results are ordered by newest first.
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, plot_name, description, distribution_type, parameters
                FROM Plots
                WHERE owner_id = :owner_id
                ORDER BY created DESC
            """),
            {"owner_id": owner_id}
        )

        return result.fetchall()
    
def get_plot_by_id(plot_id: int):
    """
    Retrieves a single saved plot by its ID.

    Returns:
        tuple: Plot record or None
    """
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, plot_name, description,
                       distribution_type, parameters
                FROM Plots
                WHERE id = :plot_id
            """),
            {"plot_id": plot_id}
        ).fetchone()

        return result
    
def delete_plot(plot_id: int):
    """
    Deletes a plot by ID.
    """
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM Plots WHERE id = :plot_id"),
            {"plot_id": plot_id}
        )
        conn.commit()
    
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
