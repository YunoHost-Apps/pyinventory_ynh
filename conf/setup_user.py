from inventory.permissions import get_or_create_normal_user_group


def setup_project_user(user):
    """
    All users used the Django admin, so we need to set the "staff" user flag.
    Called from django_yunohost_integration.sso_auth
    """
    pyinventory_user_group = get_or_create_normal_user_group()[0]
    user.groups.set([pyinventory_user_group])

    user.is_staff = True
    user.save()
    return user
