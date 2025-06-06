import re


def validate_username(username: str) -> tuple[bool, list[str]]:
    """
    Gebruikersnaam requirements:
    - 8-10 tekens
    - Moet beginnen met een letter of underscore
    - Mag letters, cijfers, underscores, punten en apostrofs bevatten
    - Niet hoofdlettergevoelig
    """
    errors = []

    if not (8 <= len(username) <= 10):
        errors.append("Username must be between 8 and 10 characters long.")
    if not re.match(r"^[A-Za-z_]", username):
        errors.append("Username must start with a letter or underscore.")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_'.]{7,9}$", username):
        errors.append("Username can only contain letters, digits, underscore (_), apostrophe ('), and period (.)")

    return len(errors) == 0, errors


def validate_password(password: str) -> tuple[bool, list[str]]:
    """
    Wachtwoord requirements:
    - 12-30 tekens
    - Minstens 1 hoofdletter, 1 kleine letter, 1 cijfer en 1 speciaal teken
    """
    errors = []

    if len(password) < 12:
        errors.append("Password must be at least 12 characters.")
    if len(password) > 30:
        errors.append("Password must be no more than 30 characters.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[~!@#$%&_+\-=`|\\(){}[\]:;'<>,.?/]", password):
        errors.append("Password must contain at least one special character.")

    return len(errors) == 0, errors


def validate_name(name: str) -> tuple[bool, list[str]]:
    errors = []
    if not name:
        errors.append("Name cannot be empty.")
    elif not re.match(r"^[A-Za-z]+(?:[-\s][A-Za-z]+)*$", name):
        errors.append("Name can only contain letters, spaces, and hyphens (no numbers or special characters).")

    return (len(errors) == 0, errors)


def validate_zip_code(zip_code: str) -> bool:
    # Nederlandse postcode: 4 cijfers + 2 hoofdletters
    return re.match(r"^\d{4}[A-Z]{2}$", zip_code) is not None


def validate_phone_number(phone: str) -> bool:
    # Telefoon format: DDDDDDDD (8 cijfers na +31-6-)
    return re.match(r"^\d{8}$", phone) is not None


def validate_driving_license(license_number: str) -> bool:
    # RegEx voor een rijbewijs: XXDDDDDDD of XDDDDDDDD
    return re.match(r"^[A-Z]{1,2}\d{7}$", license_number) is not None


def validate_latitude(lat: float) -> bool:
    # Rotterdam heeft een latitude van ongeveer 51.8 ~ 52.0
    return 51.8 <= lat <= 52.0


def validate_longitude(lon: float) -> bool:
    # Rotterdam heeft een longitude van ongeveer 4.3 ~ 4.6
    return 4.3 <= lon <= 4.6


def validate_soc_percentage(value: int) -> bool:
    # State of Charge (SoC) range
    return 0 <= value <= 100


def validate_iso_date(date_str: str) -> bool:
    # Dateformat YYYY-MM-DD
    return re.match(r"^\d{4}-\d{2}-\d{2}$", date_str) is not None
