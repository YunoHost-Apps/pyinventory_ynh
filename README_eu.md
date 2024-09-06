<!--
Ohart ongi: README hau automatikoki sortu da <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>ri esker
EZ editatu eskuz.
-->

# PyInventory YunoHost-erako

[![Integrazio maila](https://dash.yunohost.org/integration/pyinventory.svg)](https://ci-apps.yunohost.org/ci/apps/pyinventory/) ![Funtzionamendu egoera](https://ci-apps.yunohost.org/ci/badges/pyinventory.status.svg) ![Mantentze egoera](https://ci-apps.yunohost.org/ci/badges/pyinventory.maintain.svg)

[![Instalatu PyInventory YunoHost-ekin](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Irakurri README hau beste hizkuntzatan.](./ALL_README.md)*

> *Pakete honek PyInventory YunoHost zerbitzari batean azkar eta zailtasunik gabe instalatzea ahalbidetzen dizu.*  
> *YunoHost ez baduzu, kontsultatu [gida](https://yunohost.org/install) nola instalatu ikasteko.*

## Aurreikuspena

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Paketatutako bertsioa:** 0.20.1~ynh1

## Pantaila-argazkiak

![PyInventory(r)en pantaila-argazkia](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![PyInventory(r)en pantaila-argazkia](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![PyInventory(r)en pantaila-argazkia](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![PyInventory(r)en pantaila-argazkia](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Dokumentazioa eta baliabideak

- Jatorrizko aplikazioaren kode-gordailua: <https://github.com/jedie/PyInventory/>
- YunoHost Denda: <https://apps.yunohost.org/app/pyinventory>
- Eman errore baten berri: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Garatzaileentzako informazioa

Bidali `pull request`a [`testing` abarrera](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

`testing` abarra probatzeko, ondorengoa egin:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
edo
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Informazio gehiago aplikazioaren paketatzeari buruz:** <https://yunohost.org/packaging_apps>
