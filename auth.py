import re
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, UserProfile

def validate_password(password):
    """
    Validates that a password is:
    - At least 6 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    return True, "Password is valid."

def create_user(username, email, password, fullname=None, phone=None, is_admin=False):
    # Check if user already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        if existing_user.username == username:
            return None, "Username already exists."
        else:
            return None, "Email address already registered."

    # Validate password
    valid, message = validate_password(password)
    if not valid:
        return None, message

    # Hash password and create record
    hashed_pwd = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_pwd, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()

    # Create associated profile
    profile = UserProfile(user_id=new_user.id, fullname=fullname or username.title(), phone=phone, preferences="{}")
    db.session.add(profile)
    db.session.commit()

    return new_user, "User registered successfully."

def verify_user(username_or_email, password):
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user:
        return None, "Username or Email not found."
    
    if check_password_hash(user.password_hash, password):
        return user, "Logged in successfully."
    else:
        return None, "Incorrect password."
