# PyInventory for YunoHost

[![Integration level](https://dash.yunohost.org/integration/pyinventory.svg)](https://dash.yunohost.org/appci/app/pyinventory) ![](https://ci-apps.yunohost.org/ci/badges/pyinventory.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/pyinventory.maintain.svg)  
[![Install PyInventory with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

> *This package allows you to install PyInventory quickly and simply on a YunoHost server.
If you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*

Pull requests welcome ;)

## Overview

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using Python/Django.

## Screenshots

![](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.2.0%20screenshot%201.png)
![](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.1.0%20screenshot%202.png)
![](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.1.0%20screenshot%203.png)


## Settings and upgrades

Almost everything related to PyInventory's configuration is handled in a `"../conf/settings.py"` file.
You can edit the file `/opt/yunohost/pyinventory/local_settings.py` to enable or disable features.

Test sending emails:

```bash
ssh admin@yourdomain.tld
root@yunohost:~# cd /opt/yunohost/pyinventory/
root@yunohost:/opt/yunohost/pyinventory# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/pyinventory# ./manage.py sendtestemail --admins
```

Background info: Error mails are send to all [settings.ADMINS](https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-ADMINS). By default the YunoHost admin is inserted here.
To check current ADMINS run:

```bash
(venv) root@yunohost:/opt/yunohost/pyinventory# ./manage.py sendtestemail --admins
```

If you prefere to send error emails to a extrnal email address, just do something like this:

```bash
echo "ADMINS = (('Your Name', 'example@domain.tld'),)" >> /opt/yunohost/pyinventory/local_settings.py
```

To check the effective settings, run this:
```bash
(venv) root@yunohost:/opt/yunohost/pyinventory# ./manage.py diffsettings
```


# Miscellaneous


## SSO authentication

[SSOwat](https://github.com/YunoHost/SSOwat) is fully supported via [django_ynh](https://github.com/YunoHost-Apps/django_ynh):

* First user (`$YNH_APP_ARG_ADMIN`) will be created as Django's super user
* All new users will be created as normal users
* Login via SSO is fully supported
* User Email, First / Last name will be updated from SSO data


## Links

 * Report a bug about this package: https://github.com/YunoHost-Apps/pyinventory_ynh
 * Report a bug about PyInventory itself: https://github.com/jedie/PyInventory
 * YunoHost website: https://yunohost.org/

---

# Developer info

## package installation / debugging

Please send your pull request to https://github.com/YunoHost-Apps/pyinventory_ynh

Try 'main' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/master --debug
or
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/master --debug
```

Try 'testing' branch, e.g.:
```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
or
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

To remove call e.g.:
```bash
sudo yunohost app remove pyinventory
```

Backup / remove / restore cycle, e.g.:
```bash
yunohost backup create --apps pyinventory
yunohost backup list
archives:
  - pyinventory-pre-upgrade1
  - 20201223-163434
yunohost app remove pyinventory
yunohost backup restore 20201223-163434 --apps pyinventory
```

Debug installation, e.g.:
```bash
root@yunohost:~# ls -la /var/www/pyinventory/
total 18
drwxr-xr-x 4 root root 4 Dec  8 08:36 .
drwxr-xr-x 6 root root 6 Dec  8 08:36 ..
drwxr-xr-x 2 root root 2 Dec  8 08:36 media
drwxr-xr-x 7 root root 8 Dec  8 08:40 static

root@yunohost:~# ls -la /opt/yunohost/pyinventory/
total 58
drwxr-xr-x 5 pyinventory pyinventory   11 Dec  8 08:39 .
drwxr-xr-x 3 root        root           3 Dec  8 08:36 ..
-rw-r--r-- 1 pyinventory pyinventory  460 Dec  8 08:39 gunicorn.conf.py
-rw-r--r-- 1 pyinventory pyinventory    0 Dec  8 08:39 local_settings.py
-rwxr-xr-x 1 pyinventory pyinventory  274 Dec  8 08:39 manage.py
-rw-r--r-- 1 pyinventory pyinventory  171 Dec  8 08:39 secret.txt
drwxr-xr-x 6 pyinventory pyinventory    6 Dec  8 08:37 venv
-rw-r--r-- 1 pyinventory pyinventory  115 Dec  8 08:39 wsgi.py
-rw-r--r-- 1 pyinventory pyinventory 4737 Dec  8 08:39 settings.py

root@yunohost:~# cd /opt/yunohost/pyinventory/
root@yunohost:/opt/yunohost/pyinventory# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/pyinventory# ./manage.py check
PyInventory v0.8.2 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='settings'
PROJECT_PATH:/opt/yunohost/pyinventory/venv/lib/python3.7/site-packages
BASE_PATH:/opt/yunohost/pyinventory
System check identified no issues (0 silenced).

root@yunohost:~# tail -f /var/log/pyinventory/pyinventory.log
root@yunohost:~# cat /etc/systemd/system/pyinventory.service

root@yunohost:~# systemctl reload-or-restart pyinventory
root@yunohost:~# journalctl --unit=pyinventory --follow
```

## local test

For quicker developing of PyInventory in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/YunoHost-Apps/pyinventory_ynh.git
~$ cd pyinventory_ynh/
~/pyinventory_ynh$ make
install-poetry         install or update poetry
install                install PyInventory via poetry
update                 update the sources and installation
local-test             Run local_test.py to run pyinventory_ynh locally
~/pyinventory_ynh$ make install-poetry
~/pyinventory_ynh$ make install
~/pyinventory_ynh$ make local-test
```

Notes:

* SQlite database will be used
* A super user with username `test` and password `test` is created
* The page is available under `http://127.0.0.1:8000/app_path/`
