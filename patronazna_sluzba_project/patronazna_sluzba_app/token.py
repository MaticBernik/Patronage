from datetime import datetime, timedelta

import cryptography
from cryptography.fernet import Fernet

FERNET_KEY = 'H-gvBa31So7ZWRlIleY7q5xYPIytGnRHRcBpRbASyao='
fernet = Fernet(FERNET_KEY)

DATE_FORMAT = '%Y-%m-%d %H-%M-%S'
EXPIRATION_DAYS = 1


def _get_time():
    # vrne string s trenutnim utc casom
    return datetime.utcnow().strftime(DATE_FORMAT)


def _parse_time( d):
    # vrne datetime objekt
    return datetime.strptime(d, DATE_FORMAT)


def generate_token(text):
    #   generira token
    full_text = text + '|' + _get_time()
    token = fernet.encrypt(bytes(full_text), 'utf-8')

    return token


def get_token_value(token):
    # vrne none ce token ni kul al pa je expired
    try:
        value = fernet.decrypt(bytes(token, 'utf-8')).decode("utf-8")
        separator_pos = value.rfind('|')

        text = value[: separator_pos]
        token_time = _parse_time(value[separator_pos + 1:])

        if token_time + timedelta(EXPIRATION_DAYS) < datetime.utcnow():
            return None

    except cryptography.fernet.InvalidToken:
        return None

    return text


def is_valid_token(token):
    text = get_token_value(token)
    if text is not None:
        return text
    else:
        return False
