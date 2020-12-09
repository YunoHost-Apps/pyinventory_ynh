#!/usr/bin/env python3
import argparse
import os
import sys


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'ynh_pyinventory_settings'

    parser = argparse.ArgumentParser(
        description='Create or update Django super user.'
    )
    parser.add_argument('--username')
    parser.add_argument('--email')
    parser.add_argument('--password')

    args = parser.parse_args()
    username = args.username
    email = args.email or ''
    password = args.password

    import django
    django.setup()

    from django.contrib.auth import get_user_model
    User = get_user_model()
    super_user = User.objects.filter(username=username).first()
    if super_user:
        print('Update existing super user and set his password.', file=sys.stderr)
        super_user.set_password(password)
        super_user.email=email
        super_user.save()
    else:
        print('Create new super user', file=sys.stderr)
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )


if __name__ == '__main__':
    main()
