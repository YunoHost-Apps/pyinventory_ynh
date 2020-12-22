"""
    * remote user authentication backend
    * remote user middleware

    Note: SSOwat/nginx add authentication headers:

        'HTTP_AUTHORIZATION': 'Basic XXXXXXXXXXXXXXXX='
        'HTTP_AUTH_USER': 'username'
        'HTTP_REMOTE_USER': 'username'

    Basic auth contains "{username}:{plaintext-password}"

    and we get SSOwat cookies like:

         'HTTP_COOKIE': 'SSOwAuthUser=username; '
                        'SSOwAuthHash=593876aa66...99e69f88af1e; '
                        'SSOwAuthExpire=1609227697.998; '

    * Login a user via HTTP_REMOTE_USER header, but check also username in:
        * SSOwAuthUser
        * HTTP_AUTH_USER
        * HTTP_AUTHORIZATION (Basic auth)
    * Create new users
    * Update Email, First / Last name for existing users
"""
import base64
import logging

from axes.exceptions import AxesBackendPermissionDenied
from django.contrib.auth.backends import RemoteUserBackend as OriginRemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware as OriginRemoteUserMiddleware
from django.core.exceptions import ValidationError
from inventory.permissions import get_or_create_normal_user_group

logger = logging.getLogger(__name__)


def update_user_profile(request):
    """
    Update existing user information:
     * Email
     * First / Last name
    """
    user = request.user
    assert user.is_authenticated

    update_fields = []

    if not user.password:
        # Empty password is not valid, so we can't save the model, because of full_clean() call
        logger.info('Set unusable password for user: %s', user)
        user.set_unusable_password()
        update_fields.append('password')

    email = request.META.get('HTTP_EMAIL')
    if email and user.email != email:
        logger.info('Update email: %r -> %r', user.email, email)
        user.email = email
        update_fields.append('email')

    raw_username = request.META.get('HTTP_NAME')
    if raw_username:
        if ' ' in raw_username:
            first_name, last_name = raw_username.split(' ', 1)
        else:
            first_name = ''
            last_name = raw_username

        if user.first_name != first_name:
            logger.info('Update first name: %r -> %r', user.first_name, first_name)
            user.first_name = first_name
            update_fields.append('first_name')

        if user.last_name != last_name:
            logger.info('Update last name: %r -> %r', user.last_name, last_name)
            user.last_name = last_name
            update_fields.append('last_name')

    if update_fields:
        try:
            user.full_clean()
        except ValidationError:
            logger.exception('Can not update user: %s', user)
        else:
            user.save(update_fields=update_fields)


class RemoteUserMiddleware(OriginRemoteUserMiddleware):
    """
    Middleware to login a user HTTP_REMOTE_USER header.
    Use Django Axes if something is wrong.
    Update exising user informations.
    """
    header = 'HTTP_REMOTE_USER'
    force_logout_if_no_header = True

    def process_request(self, request):
        # Keep the information if the user is already logged in
        was_authenticated = request.user.is_authenticated

        super().process_request(request)  # login remote user

        if not request.user.is_authenticated:
            # Not logged in -> nothing to verify here
            return

        # Check SSOwat cookie informations:
        try:
            username = request.COOKIES['SSOwAuthUser']
        except KeyError:
            logger.error('SSOwAuthUser cookie missing!')

            # emits a signal indicating user login failed, which is processed by
            # axes.signals.log_user_login_failed which logs and flags the failed request.
            raise AxesBackendPermissionDenied('Cookie missing')

        logger.info('SSOwat username from cookies: %r', username)
        if username != request.user.username:
            raise AxesBackendPermissionDenied('Wrong username')

        # Compare with HTTP_AUTH_USER
        try:
            username = request.META['HTTP_AUTH_USER']
        except KeyError:
            logger.error('HTTP_AUTH_USER missing!')
            raise AxesBackendPermissionDenied('No HTTP_AUTH_USER')

        if username != request.user.username:
            raise AxesBackendPermissionDenied('Wrong HTTP_AUTH_USER username')

        # Also check 'HTTP_AUTHORIZATION', but only the username ;)
        try:
            auth = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            logger.error('HTTP_AUTHORIZATION missing!')
            raise AxesBackendPermissionDenied('No HTTP_AUTHORIZATION')

        scheme, creds = auth.split(' ', 1)
        if scheme.lower() != 'basic':
            logger.error('HTTP_AUTHORIZATION with %r not supported', scheme)
            raise AxesBackendPermissionDenied('HTTP_AUTHORIZATION scheme not supported')

        creds = str(base64.b64decode(creds), encoding='utf-8')
        username = creds.split(':', 1)[0]
        if username != request.user.username:
            raise AxesBackendPermissionDenied('Wrong HTTP_AUTHORIZATION username')

        if not was_authenticated:
            # First request, after login -> update user informations
            logger.info('Remote used was logged in')
            update_user_profile(request)


class RemoteUserBackend(OriginRemoteUserBackend):
    """
    Authentication backend via SSO/nginx header
    """
    create_unknown_user = True

    def authenticate(self, request, remote_user):
        logger.info('Remote user authenticate: %r', remote_user)
        return super().authenticate(request, remote_user)

    def configure_user(self, request, user):
        """
        Configure a user after creation and return the updated user.
        Setup a normal, non-superuser
        """
        logger.warning('Configure user %s', user)

        user.set_unusable_password()  # Always login via SSO
        user.is_staff = True
        user.is_superuser = False
        user.save()

        pyinventory_user_group = get_or_create_normal_user_group()[0]
        user.groups.set([pyinventory_user_group])

        update_user_profile(request)

        return user

    def user_can_authenticate(self, user):
        logger.warning('Remote user login: %s', user)
        return True
