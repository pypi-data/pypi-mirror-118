from django.conf import settings

if settings.SHA_ACCOUNTS.get('AUTH_USER_MODEL') == 'User':
    from .permission_models import Permission
    from .profile_models import Profile
    from .user_models import User
