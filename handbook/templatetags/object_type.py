from django import template

register = template.Library()


def object_type(obj):
    return obj.__class__.__name__


register.filter(object_type)
