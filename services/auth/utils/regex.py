import re

password_regex = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def is_valid_email(email: str) -> bool:
    return re.fullmatch(email_regex, email) is not None

def is_valid_password(password: str) -> bool:
    return re.fullmatch(password_regex, password) is not None