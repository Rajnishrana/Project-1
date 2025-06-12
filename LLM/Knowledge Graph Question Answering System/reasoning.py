
from datetime import datetime

def calculate_age(birth_date: str, death_date: str = None) -> int:
    """
    Calculate age based on birth date and optionally death date.
    """
    birth = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%SZ")

    if death_date:
        death = datetime.strptime(death_date, "%Y-%m-%dT%H:%M:%SZ")
        age = death.year - birth.year - ((death.month, death.day) < (birth.month, birth.day))
    else:
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    return age
