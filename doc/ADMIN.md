## Settings and upgrades

Almost everything related to PyInventory's configuration is handled in a `"../conf/settings.py"` file.
You can edit the file `/home/yunohost.app/django_example/local_settings.py` to enable or disable features.

Test sending emails, e.g.:

```bash
ssh admin@yourdomain.tld
root@yunohost:~# /home/yunohost.app/pyinventory/manage.py sendtestemail --admins
```

How to debug a django YunoHost app, take a look into:

* https://github.com/YunoHost-Apps/pyinventory_ynh#developer-info

## local test

For quicker developing of pyinventory_ynh in the context of YunoHost app,
it's possible to run the Django developer server with the settings
and urls made for YunoHost installation.

e.g.:
```bash
~$ git clone https://github.com/YunoHost-Apps/django_example.git
~$ cd pyinventory_ynh/
~/django_example$ ./dev-cli.py --help
```


The output will looks like:

[comment]: <> (✂✂✂ auto generated help start ✂✂✂)
```
Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run tests and show coverage report.                                  │
│ diffsettings                Run "diffsettings" manage command against a "local_test" YunoHost    │
│                             installation.                                                        │
│ fix-code-style              Fix code style of all pyinventory_ynh source code files via darker   │
│ install                     Run pip-sync and install 'pyinventory_ynh' via pip as editable.      │
│ local-test                  Build a "local_test" YunoHost installation and start the Django dev. │
│                             server against it.                                                   │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ pip-audit                   Run pip-audit check against current requirements files               │
│ publish                     Build and upload this project to PyPi                                │
│ test                        Compile YunoHost files and run Django unittests                      │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated help end ✂✂✂)
