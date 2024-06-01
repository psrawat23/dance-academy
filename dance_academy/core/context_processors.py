from django.conf import settings  # import the settings file


def site_settings(request):
    # returning the bluered web setting values
    return {"SITE_WEB_SETTINGS": settings.SITE_WEB_SETTINGS}


def get_setting(request):
    return {"SETTING": settings}
