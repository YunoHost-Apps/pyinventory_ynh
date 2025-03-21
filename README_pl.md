<!--
To README zostało automatycznie wygenerowane przez <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
Nie powinno być ono edytowane ręcznie.
-->

# PyInventory dla YunoHost

[![Poziom integracji](https://apps.yunohost.org/badge/integration/pyinventory)](https://ci-apps.yunohost.org/ci/apps/pyinventory/)
![Status działania](https://apps.yunohost.org/badge/state/pyinventory)
![Status utrzymania](https://apps.yunohost.org/badge/maintained/pyinventory)

[![Zainstaluj PyInventory z YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Przeczytaj plik README w innym języku.](./ALL_README.md)*

> *Ta aplikacja pozwala na szybką i prostą instalację PyInventory na serwerze YunoHost.*
> *Jeżeli nie masz YunoHost zapoznaj się z [poradnikiem](https://yunohost.org/install) instalacji.*

## Przegląd

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Dostarczona wersja:** 0.21.0~ynh3

## Zrzuty ekranu

![Zrzut ekranu z PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Zrzut ekranu z PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Zrzut ekranu z PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![Zrzut ekranu z PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Dokumentacja i zasoby

- Repozytorium z kodem źródłowym: <https://github.com/jedie/PyInventory>
- Sklep YunoHost: <https://apps.yunohost.org/app/pyinventory>
- Zgłaszanie błędów: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Informacje od twórców

Wyślij swój pull request do [gałęzi `testing`](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Aby wypróbować gałąź `testing` postępuj zgodnie z instrukcjami:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
lub
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Więcej informacji o tworzeniu paczek aplikacji:** <https://yunohost.org/packaging_apps>
