# forum/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def filter_apartment(votes, apartment):
    return votes.filter(apartment=apartment).exists()