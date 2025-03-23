<!--
N.B.: README ini dibuat secara otomatis oleh <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
Ini TIDAK boleh diedit dengan tangan.
-->

# PyInventory untuk YunoHost

[![Tingkat integrasi](https://apps.yunohost.org/badge/integration/pyinventory)](https://ci-apps.yunohost.org/ci/apps/pyinventory/)
![Status kerja](https://apps.yunohost.org/badge/state/pyinventory)
![Status pemeliharaan](https://apps.yunohost.org/badge/maintained/pyinventory)

[![Pasang PyInventory dengan YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Baca README ini dengan bahasa yang lain.](./ALL_README.md)*

> *Paket ini memperbolehkan Anda untuk memasang PyInventory secara cepat dan mudah pada server YunoHost.*  
> *Bila Anda tidak mempunyai YunoHost, silakan berkonsultasi dengan [panduan](https://yunohost.org/install) untuk mempelajari bagaimana untuk memasangnya.*

## Ringkasan

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Versi terkirim:** 0.21.0~ynh1

## Tangkapan Layar

![Tangkapan Layar pada PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Tangkapan Layar pada PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Tangkapan Layar pada PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![Tangkapan Layar pada PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Dokumentasi dan sumber daya

- Depot kode aplikasi hulu: <https://github.com/jedie/PyInventory>
- Gudang YunoHost: <https://apps.yunohost.org/app/pyinventory>
- Laporkan bug: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Info developer

Silakan kirim pull request ke [`testing` branch](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Untuk mencoba branch `testing`, silakan dilanjutkan seperti:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
atau
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Info lebih lanjut mengenai pemaketan aplikasi:** <https://yunohost.org/packaging_apps>
