<!--
Важно: этот README был автоматически сгенерирован <https://github.com/YunoHost/apps/tree/master/tools/readme_generator>
Он НЕ ДОЛЖЕН редактироваться вручную.
-->

# PyInventory для YunoHost

[![Уровень интеграции](https://dash.yunohost.org/integration/pyinventory.svg)](https://ci-apps.yunohost.org/ci/apps/pyinventory/) ![Состояние работы](https://ci-apps.yunohost.org/ci/badges/pyinventory.status.svg) ![Состояние сопровождения](https://ci-apps.yunohost.org/ci/badges/pyinventory.maintain.svg)

[![Установите PyInventory с YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=pyinventory)

*[Прочтите этот README на других языках.](./ALL_README.md)*

> *Этот пакет позволяет Вам установить PyInventory быстро и просто на YunoHost-сервер.*  
> *Если у Вас нет YunoHost, пожалуйста, посмотрите [инструкцию](https://yunohost.org/install), чтобы узнать, как установить его.*

## Обзор

[![tests](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/YunoHost-Apps/pyinventory_ynh/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/pyinventory_ynh/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/pyinventory_ynh)
[![pyinventory_ynh @ PyPi](https://img.shields.io/pypi/v/pyinventory_ynh?label=pyinventory_ynh%20%40%20PyPi)](https://pypi.org/project/pyinventory_ynh/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/pyinventory_ynh)](https://github.com/YunoHost-Apps/pyinventory_ynh/blob/main/LICENSE)

[PyInventory](https://github.com/jedie/PyInventory) is a libre web-based management to catalog things including state and location etc. using [Python](https://www.python.org/)/[Django](https://www.djangoproject.com/).

Pull requests welcome ;)

This package for YunoHost used [django-yunohost-integration](https://github.com/YunoHost-Apps/django_yunohost_integration)

More screenshots are here: jedie.github.io/tree/master/screenshots/PyInventory


**Поставляемая версия:** 0.20.1~ynh1

## Снимки экрана

![Снимок экрана PyInventory](./doc/screenshots/pyinventory_v010_screenshot_2.png)
![Снимок экрана PyInventory](./doc/screenshots/pyinventory_v010_screenshot_3.png)
![Снимок экрана PyInventory](./doc/screenshots/pyinventory_v0110_screenshot_memo_1.png)
![Снимок экрана PyInventory](./doc/screenshots/pyinventory_v020_screenshot_1.png)

## Документация и ресурсы

- Репозиторий кода главной ветки приложения: <https://github.com/jedie/PyInventory/>
- Магазин YunoHost: <https://apps.yunohost.org/app/pyinventory>
- Сообщите об ошибке: <https://github.com/YunoHost-Apps/pyinventory_ynh/issues>

## Информация для разработчиков

Пришлите Ваш запрос на слияние в [ветку `testing`](https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing).

Чтобы попробовать ветку `testing`, пожалуйста, сделайте что-то вроде этого:

```bash
sudo yunohost app install https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
или
sudo yunohost app upgrade pyinventory -u https://github.com/YunoHost-Apps/pyinventory_ynh/tree/testing --debug
```

**Больше информации о пакетировании приложений:** <https://yunohost.org/packaging_apps>
