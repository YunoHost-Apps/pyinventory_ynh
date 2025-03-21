## Setup Python Interpreter

To use a more recent Python version than the current debian stable release,
we use two ways:

* ["install_python.py" will compile and install Python from source, if needed](https://github.com/jedie/manageprojects/blob/main/docs/install_python.md)
* ["setup_python.py" will download and setup redistributable Python from [1] if needed.](https://github.com/jedie/manageprojects/blob/main/docs/setup_python.md) (default)

[1] https://github.com/indygreg/python-build-standalone/

Both variants will use the OS version of Python, if it's already the requested major version.
And both will install the needed Python version only one time.

Compile from source will take significantly longer than the redistributable version.

It's possible to switch between the two variants on installation.

Discuss this here: https://forum.yunohost.org/t/use-newer-python-than-3-9/22568/17

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
usage: ./dev-cli.py [-h]
                    {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,update-te
st-snapshot-files,version}



╭─ options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ -h, --help        show this help message and exit                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ subcommands ──────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {check-code-style,coverage,fix-code-style,install,mypy,nox,pip-audit,publish,test,update,update-test-snapshot-file │
│ s,version}                                                                                                         │
│     check-code-style                                                                                               │
│                   Check code style by calling darker + flake8                                                      │
│     coverage      Run tests and show coverage report.                                                              │
│     fix-code-style                                                                                                 │
│                   Fix code style of all pyinventory_ynh source code files via darker                               │
│     install       Install requirements and 'pyinventory_ynh' via pip as editable.                                  │
│     mypy          Run Mypy (configured in pyproject.toml)                                                          │
│     nox           Run nox                                                                                          │
│     pip-audit     Run pip-audit check against current requirements files                                           │
│     publish       Build and upload this project to PyPi                                                            │
│     test          Run unittests                                                                                    │
│     update        Update "requirements*.txt" dependencies files                                                    │
│     update-test-snapshot-files                                                                                     │
│                   Update all test snapshot files (by remove and recreate all snapshot files)                       │
│     version       Print version and exit                                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated help end ✂✂✂)
