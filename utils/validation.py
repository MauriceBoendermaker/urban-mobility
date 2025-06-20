import re

from travellers.cities import CITIES
from datetime import datetime


def validate_city_number(user_input: str) -> tuple[bool, list[str]]:
    try:
        city_number = int(user_input)
        if city_number not in range(1, len(CITIES) + 1):
            return (False, [f"Enter the number of the city (1-{len(CITIES)}): "])
        return (True, [""])

    except:
        return (False, [""])


def validate_street_name(street_name: str) -> tuple[bool, list[str]]:
    errors = []
    if not re.match(r"^[A-Za-z][A-Za-z\s\-]*$", street_name):
        errors.append(
            "Street name must start with letters and may only contain a dash (-)")
    return len(errors) == 0, errors


def validate_house_number(house_number: str) -> tuple[bool, list[str]]:
    errors = []

    if not re.fullmatch(r"\d{1,3}[A-Za-z]?", house_number):
        errors.append("house number can only contain 1-3 digits")

    return len(errors) == 0, errors


def validate_gender(gender: str) -> tuple[bool, list[str]]:
    errors = []

    if not re.fullmatch(r"[MFmf]?", gender):
        errors.append("Choose 'M' or 'm' for male, and 'F' or 'f' for female")
    return len(errors) == 0, errors


def validate_email_address(email_address: str) -> tuple[bool, list[str]]:
    """
    Validates an email address.
    Requirements:
    - Must follow basic email format: local@domain.tld
    - Local part can contain letters, numbers, dots, underscores, dashes, and plus signs
    - local part cannot start with special characters
    - Domain and TLD must be alphanumeric (dots and dashes allowed in domain)
    """

    errors = []

    pattern = (
        r"^(?![_.+-])"
        r"[a-zA-Z0-9]+([._+-]?[a-zA-Z0-9]+)*"
        r"@"
        r"[a-zA-Z0-9-]+"
        r"(\.[a-zA-Z0-9-]+)*"
        r"\.[a-zA-Z]{2,}$")

    if not re.fullmatch(pattern, email_address):
        errors.append("Invalid email format. Must be like 'name@example.com'.")

    return len(errors) == 0, errors


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
        errors.append(
            "Username can only contain letters, digits, underscore (_), apostrophe ('), and period (.)")

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
        errors.append(
            "Name can only contain letters, spaces, and hyphens (no numbers or special characters).")

    return (len(errors) == 0, errors)


def validate_zip_code(zip_code: str) -> bool:
    # Nederlandse postcode: 4 cijfers + 2 hoofdletters
    return re.match(r"^\d{4}[A-Z]{2}$", zip_code) is not None


def validate_phone_number(phone: str) -> bool:
    # Telefoon format: DDDDDDDD (8 cijfers na +31-6-)
    return re.match(r"^\d{8}$", phone) is not None


def validate_driving_license(license_number: str) -> tuple[bool, list[str]]:
    # RegEx voor een rijbewijs: XXDDDDDDD of XDDDDDDDD
    errors = []
    if not re.fullmatch(r"[A-Z]{1,2}\d{7}", license_number):
        errors.append("Driving license number must match the format: XX1234567 or X1234567")
    return len(errors) == 0, errors


def validate_latitude(value: str) -> tuple[bool, list[str]]:
    # Rotterdam heeft een latitude van ongeveer 51.8 ~ 52.0
    errors = []
    try:
        lat = float(value)
        if not (51.8 <= lat <= 52.0):
            errors.append("Latitude must be between 51.8 and 52.0 (Rotterdam region).")
    except ValueError:
        errors.append("Latitude must be a valid number.")
    return len(errors) == 0, errors


def validate_longitude(value: str) -> tuple[bool, list[str]]:
    # Rotterdam heeft een longitude van ongeveer 4.3 ~ 4.6
    errors = []
    try:
        lon = float(value)
        if not (4.3 <= lon <= 4.6):
            errors.append("Longitude must be between 4.3 and 4.6 (Rotterdam region).")
    except ValueError:
        errors.append("Longitude must be a valid number.")
    return len(errors) == 0, errors


def validate_soc_percentage(value: str) -> tuple[bool, list[str]]:
    # State of Charge (SoC) range
    errors = []
    try:
        val = int(value)
        if not (0 <= val <= 100):
            errors.append("Value must be between 0 and 100.")
    except ValueError:
        errors.append("Value must be a number.")
    return len(errors) == 0, errors


def validate_serial_number(serial: str) -> tuple[bool, list[str]]:
    errors = []
    if not (10 <= len(serial) <= 17):
        errors.append("Serial number must be between 10 and 17 characters.")
    if not re.fullmatch(r"[A-Za-z0-9]{10,17}", serial):
        errors.append("Serial number must be alphanumeric.")
    return len(errors) == 0, errors


def validate_iso_date(date_str: str) -> tuple[bool, list[str]]:
    errors = []
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True, []
    except ValueError:
        errors.append("Date must follow format YYYY-MM-DD.")
        return False, errors


def validate_positive_int(value: str) -> tuple[bool, list[str]]:
    errors = []
    try:
        int_value = int(value)
        if int_value <= 0:
            errors.append("Value must be greater than 0.")
    except ValueError:
        errors.append("Value must be a valid number.")
    return len(errors) == 0, errors


def get_valid_input(prompt, validator, error_label, toupper=False):
    while True:
        if toupper:
            value = input(prompt).strip().upper()
        else:
            value = input(prompt).strip()
        result = validator(value)

        if isinstance(result, bool):
            valid, errors = result, []
        else:
            valid, errors = result

        if valid:
            return value

        print(f"{error_label}:")
        for error in errors:
            print(" -", error)
