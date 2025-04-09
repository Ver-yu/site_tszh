from django import template
from ..models import Vote

register = template.Library()

@register.filter(name='has_voted')
def has_voted(option, apartment):
    return Vote.objects.filter(option=option, apartment=apartment).exists()
