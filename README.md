# PyInventory for YunoHost

[![Integration level](https://dash.yunohost.org/integration/pyinventory.svg)](https://dash.yunohost.org/appci/app/pyinventory) ![](https://ci-apps.yunohost.org/ci/badges/pyinventory.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/pyinventory.maintain.svg)
[![Install PyInventory with YunoHost](https://install-app.yunohost.org/install-with-yunohost.png)](https://install-app.yunohost.org/?app=pyinventory)

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

Almost everything related to PyInventory's configuration is handled in a `"../conf/ynh_pyinventory_settings.py"` file.
You can edit the file `$final_path/local_settings.py` to enable or disable features.

# Miscellaneous

## LDAP connection

Supported by https://github.com/django-auth-ldap/django-auth-ldap

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
-rw-r--r-- 1 pyinventory pyinventory 4737 Dec  8 08:39 ynh_pyinventory_settings.py

root@yunohost:~# cd /opt/yunohost/pyinventory/
root@yunohost:/opt/yunohost/pyinventory# source venv/bin/activate
(venv) root@yunohost:/opt/yunohost/pyinventory# ./manage.py check
PyInventory v0.8.1 (Django v2.2.17)
DJANGO_SETTINGS_MODULE='ynh_pyinventory_settings'
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
