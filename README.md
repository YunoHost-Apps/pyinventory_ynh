# PyInventory for YunoHost

[![Integration level](https://dash.yunohost.org/integration/pyinventory.svg)](https://dash.yunohost.org/appci/app/pyinventory) ![](https://ci-apps.yunohost.org/ci/badges/pyinventory.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/pyinventory.maintain.svg)  
[![Install PyInventory with YunoHost](https://install-app.yunohost.org/install-with-yunohost.png)](https://install-app.yunohost.org/?app=pyinventory)

> *This package allows you to install PyInventory quickly and simply on a YunoHost server.  
If you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*

Current status is pre-alpha: This app doesn't work, yet ;)

Pull requests welcome ;)

## Overview

PyInventory is a libre web-based management to catalog things including state and location etc. using Python/Django.

## Screenshots

![](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.2.0%20screenshot%201.png)
![](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.1.0%20screenshot%202.png)
![](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/PyInventory/PyInventory%20v0.1.0%20screenshot%203.png)

## Admin account

An admin user is created at installation, the login is what you provided at installation, the password is **pyinventory**.

## Settings and upgrades

Almost everything related to PyInventory's configuration is handled in a `"../conf/ynh_pyinventory_settings.py"` file.
You can edit the file `$final_path/local_settings.py` to enable or disable features.

# Miscellaneous

## LDAP connexion

TODO: https://github.com/django-auth-ldap/django-auth-ldap

## Links

 * Report a bug about this package: https://github.com/jedie/pyinventory_ynh
 * Report a bug about PyInventory itself: https://github.com/jedie/PyInventory
 * YunoHost website: https://yunohost.org/

---

Developer info
----------------

Please send your pull request to https://github.com/jedie/pyinventory_ynh

Try e.g.:
```
sudo yunohost app install https://github.com/jedie/pyinventory_ynh/tree/main --debug
or
sudo yunohost app upgrade pyinventory -u https://github.com/jedie/pyinventory_ynh/tree/main --debug
```
