<!--
N.B.: Questo README è stato automaticamente generato da <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
NON DEVE essere modificato manualmente.
-->

# PyInventory per YunoHost

[![Livello di integrazione](https://dash.yunohost.org/integration/pyinventory.svg)](https://dash.yunohost.org/appci/app/pyinventory) ![Stato di funzionamento](https://ci-apps.yunohost.org/ci/badges/pyinventory.status.svg) ![Stato di manutenzione](https://ci-apps.yunohost.org/ci/badges/pyinventory.maintain.svg)

[![Installa PyInventory con YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Leggi questo README in altre lingue.](./ALL_README.md)*

> *Questo pacchetto ti permette di installare PyInventory su un server YunoHost in modo semplice e veloce.*  
> *Se non hai YunoHost, consulta [la guida](https://yunohost.org/install) per imparare a installarlo.*

## Panoramica

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Versione pubblicata:** 0.19.3~ynh2

## Screenshot

![Screenshot di PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Screenshot di PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Screenshot di PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)
![Screenshot di PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)

## Documentazione e risorse

- Documentazione ufficiale per gli utenti: <https://github.com/jedie/PyInventory>
- Documentazione ufficiale per gli amministratori: <https://github.com/YunoHost-Apps/pyinventory_ynh>
- Repository upstream del codice dell’app: <https://github.com/YunoHost-Apps/pyinventory_ynh>
- Store di YunoHost: <https://apps.yunohost.org/app/pyinventory>
- Segnala un problema: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Informazioni per sviluppatori

Si prega di inviare la tua pull request alla [branch di `testing`](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Per provare la branch di `testing`, si prega di procedere in questo modo:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
o
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Maggiori informazioni riguardo il pacchetto di quest’app:** <https://yunohost.org/packaging_apps>
