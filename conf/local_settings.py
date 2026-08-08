"""
    Here it's possible to overwrite everything in settings.py

    Note:
        Used for YunoHost config and will be **overwritten** on every config change!
"""

DEBUG = __DJANGO_DEBUG__  # noqa Don't turn DEBUG on in production!
