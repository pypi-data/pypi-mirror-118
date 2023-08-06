from django.conf import settings
from .signals import user_logged_in, user_logged_out, user_login_failed

if settings.SHA_ACCOUNTS.get('AUTH_USER_MODEL') == 'User':
    from .receivers import create_profile
