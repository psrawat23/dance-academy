from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def SITE_WEB_SETTINGS():
      return settings.SITE_WEB_SETTINGS