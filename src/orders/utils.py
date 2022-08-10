from time import time
from django.core.validators import RegexValidator


PHONE_NUMBER_REGEX = RegexValidator(regex = r"^\+?1?\d{8,15}$")


def uid():
    return int(str(int(time() * 10**6))[-8:])