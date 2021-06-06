from django import template
from datetime import datetime

register = template.Library()


def print_timestamp(timestamp: int):
    if timestamp < 0:
        return "Круглый год"

    try:
        temp = datetime.fromtimestamp(timestamp)
    except OSError:
        return "Круглый год"

    return temp


register.filter(print_timestamp)
