<!--
NB: Deze README is automatisch gegenereerd door <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
Hij mag NIET handmatig aangepast worden.
-->

# PyInventory voor Yunohost

[![Integratieniveau](https://apps.yunohost.org/badge/integration/pyinventory)](https://ci-apps.yunohost.org/ci/apps/pyinventory/)
![Mate van functioneren](https://apps.yunohost.org/badge/state/pyinventory)
![Onderhoudsstatus](https://apps.yunohost.org/badge/maintained/pyinventory)

[![PyInventory met Yunohost installeren](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Deze README in een andere taal lezen.](./ALL_README.md)*

> *Met dit pakket kun je PyInventory snel en eenvoudig op een YunoHost-server installeren.*
> *Als je nog geen YunoHost hebt, lees dan [de installatiehandleiding](https://yunohost.org/install), om te zien hoe je 'm installeert.*

## Overzicht

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Geleverde versie:** 0.21.2~ynh1

## Schermafdrukken

![Schermafdrukken van PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Schermafdrukken van PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Schermafdrukken van PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![Schermafdrukken van PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Documentatie en bronnen

- Upstream app codedepot: <https://github.com/jedie/PyInventory>
- YunoHost-store: <https://apps.yunohost.org/app/pyinventory>
- Meld een bug: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Ontwikkelaarsinformatie

Stuur je pull request alsjeblieft naar de [`testing`-branch](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Om de `testing`-branch uit te proberen, ga als volgt te werk:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
of
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Verdere informatie over app-packaging:** <https://yunohost.org/packaging_apps>
