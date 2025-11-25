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
    ynh_print_info "Setup Python virtualenv for $app ..."

    # Create a virtualenv
    ynh_exec_as_app python3 -m venv --upgrade-deps "$data_dir/.venv"

    # Print some version information:
    ynh_print_info "venv Python version: $($data_dir/.venv/bin/python3 -VV)"
    ynh_print_info "venv Pip version: $($data_dir/.venv/bin/python3 -m pip -V)"

    ynh_print_info "Install $app dependencies in virtualenv..."
    ynh_exec_as_app $data_dir/.venv/bin/pip3 install --upgrade pip wheel setuptools

    ynh_print_info "Install $app requirements into Python virtualenv..."

    ynh_exec_as_app $data_dir/.venv/bin/pip3 install -r "$data_dir/requirements.txt"
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
