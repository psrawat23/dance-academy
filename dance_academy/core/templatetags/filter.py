import datetime
from django import template
from django.conf import settings
import json
import ast

register = template.Library()


@register.filter(name="days_until")
def days_until(date):
    today = datetime.date.today()
    end_date = date
    if end_date == None:
        return None
    return (end_date - today).days


@register.filter(name="is_user_group")
def is_user_group(user,group):
    if user.groups.filter(name=group).exists():
        return False
    if user.is_superuser:
        return True
    return True