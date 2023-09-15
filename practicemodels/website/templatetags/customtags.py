from django import template

register = template.Library()

@register.simple_tag
def first_letter(text):
    return text.upper()

