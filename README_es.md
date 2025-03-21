<!--
Este archivo README esta generado automaticamente<https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
No se debe editar a mano.
-->

# PyInventory para Yunohost

[![Nivel de integración](https://apps.yunohost.org/badge/integration/pyinventory)](https://ci-apps.yunohost.org/ci/apps/pyinventory/)
![Estado funcional](https://apps.yunohost.org/badge/state/pyinventory)
![Estado En Mantención](https://apps.yunohost.org/badge/maintained/pyinventory)

[![Instalar PyInventory con Yunhost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Leer este README en otros idiomas.](./ALL_README.md)*

> *Este paquete le permite instalarPyInventory rapidamente y simplement en un servidor YunoHost.*
> *Si no tiene YunoHost, visita [the guide](https://yunohost.org/install) para aprender como instalarla.*

## Descripción general

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Versión actual:** 0.21.0~ynh3

## Capturas

![Captura de PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Captura de PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Captura de PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![Captura de PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Documentaciones y recursos

- Repositorio del código fuente oficial de la aplicación : <https://github.com/jedie/PyInventory>
- Catálogo YunoHost: <https://apps.yunohost.org/app/pyinventory>
- Reportar un error: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Información para desarrolladores

Por favor enviar sus correcciones a la [rama `testing`](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Para probar la rama `testing`, sigue asÍ:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
o
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Mas informaciones sobre el empaquetado de aplicaciones:** <https://yunohost.org/packaging_apps>
