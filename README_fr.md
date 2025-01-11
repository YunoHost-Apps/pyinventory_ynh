<!--
Nota bene : ce README est automatiquement généré par <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
Il NE doit PAS être modifié à la main.
-->

# PyInventory pour YunoHost

[![Niveau d’intégration](https://apps.yunohost.org/badge/integration/pyinventory)](https://ci-apps.yunohost.org/ci/apps/pyinventory/)
![Statut du fonctionnement](https://apps.yunohost.org/badge/state/pyinventory)
![Statut de maintenance](https://apps.yunohost.org/badge/maintained/pyinventory)

[![Installer PyInventory avec YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Lire le README dans d'autres langues.](./ALL_README.md)*

> *Ce package vous permet d’installer PyInventory rapidement et simplement sur un serveur YunoHost.*  
> *Si vous n’avez pas YunoHost, consultez [ce guide](https://yunohost.org/install) pour savoir comment l’installer et en profiter.*

## Vue d’ensemble

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Version incluse :** 0.20.1~ynh2

## Captures d’écran

![Capture d’écran de PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Capture d’écran de PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Capture d’écran de PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![Capture d’écran de PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Documentations et ressources

- Dépôt de code officiel de l’app : <https://github.com/jedie/PyInventory>
- YunoHost Store : <https://apps.yunohost.org/app/pyinventory>
- Signaler un bug : <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Informations pour les développeurs

Merci de faire vos pull request sur la [branche `testing`](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Pour essayer la branche `testing`, procédez comme suit :

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
ou
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Plus d’infos sur le packaging d’applications :** <https://yunohost.org/packaging_apps>
