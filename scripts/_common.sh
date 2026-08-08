#!/bin/bash

#=================================================
# RETRIEVE ARGUMENTS FROM THE MANIFEST
#=================================================

# Transfer the main SSO domain to the App:
ynh_current_host=$(cat /etc/yunohost/current_host)
__YNH_CURRENT_HOST__=${ynh_current_host}

#=================================================
# ARGUMENTS FROM CONFIG PANEL
#=================================================

# 'update_python' -> '__UPDATE_PYTHON__'
update_python="SETUP"

# 'debug_enabled' -> '__DEBUG_ENABLED__' -> settings.DEBUG
debug_enabled="0" # "1" or "0" string

# 'log_level' -> '__LOG_LEVEL__' -> settings.LOG_LEVEL
log_level="WARNING"

# 'admin_email' -> '__ADMIN_EMAIL__' add in settings.ADMINS
admin_email="${admin}@${domain}"

# 'default_from_email' -> '__DEFAULT_FROM_EMAIL__' -> settings.DEFAULT_FROM_EMAIL
default_from_email="${app}@${domain}"

#=================================================
# SET CONSTANTS
#=================================================

# e.g.: point pip cache to: /home/yunohost.app/$app/.cache/
XDG_CACHE_HOME="$data_dir/.cache/"

log_path=/var/log/$app
log_file="${log_path}/${app}.log"

#=================================================
# HELPERS
#=================================================

myynh_setup_python_venv() {
    ynh_print_info "Get latest uv via pipx for $app ..."

    export PIPX_HOME="/opt/pipx"
    export PIPX_BIN_DIR="/usr/local/bin"
    export PATH="$PIPX_BIN_DIR:$PATH"

    which pipx
    pipx install uv --force 2>&1
    pipx upgrade uv --force 2>&1
    which uv
    uv --version

    # The major Python version that should be upgrades and used:
    export UV_PYTHON="3.14"

    cd "$data_dir"

    ynh_print_info "Install/upgrade Python $UV_PYTHON via uv"
    ynh_exec_as_app uv python install --upgrade $UV_PYTHON 2>&1
    ynh_exec_as_app uv python list

    ynh_print_info "Create a virtualenv"
    ynh_exec_as_app uv venv --python $UV_PYTHON --clear "$data_dir/.venv" 2>&1
    ynh_print_info "Install Python packages from pylock.toml in virtualenv"
    ynh_exec_as_app uv pip sync "$data_dir/pylock.toml" 2>&1

    ynh_print_info "venv Python version: $($data_dir/.venv/bin/python3 -VV)"
    ynh_print_info "venv django-admin --version: $($data_dir/.venv/bin/django-admin --version)"
    ynh_print_info "venv gunicorn --version: $($data_dir/.venv/bin/gunicorn --version)"

    # The Django app worked in the venv?
    ynh_print_info "manage.py --version: $($data_dir/manage.py --version)"
    ynh_print_info "manage.py check: $($data_dir/manage.py check)"
}

myynh_setup_log_file() {
    mkdir -p "$(dirname "$log_file")"
    touch "$log_file"

    chown -c -R $app:$app "$log_path"
    chmod -c u+rwx,o-rwx "$log_path"
}

myynh_fix_file_permissions() {
    # /var/www/$app/
    # static files served by nginx, so use www-data group:
    chown -c -R "$app:www-data" "$install_dir"
    chmod -c u+rwx,g+rx,o-rwx "$install_dir"

    # /home/yunohost.app/$app/
    chown -c -R "$app:$app" "$data_dir"
    chmod -c u+rwx,g+rwx,o-rwx "$data_dir"
}
