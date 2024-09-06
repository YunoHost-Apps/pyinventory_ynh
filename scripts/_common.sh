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


#==================================================================================
# myynh_install_python() Borrowed from:
# https://github.com/YunoHost-Apps/homeassistant_ynh/blob/master/scripts/_common.sh
# Until we get a newer Python in YunoHost, see:
# https://forum.yunohost.org/t/use-newer-python-than-3-9/22568
#==================================================================================
py_required_major=3.11
py_required_version=$(curl -Ls https://www.python.org/ftp/python/ \
						| grep '>'$py_required_major  | cut -d '/' -f 2 \
						| cut -d '>' -f 2 | sort -rV | head -n 1) #3.11.8

myynh_install_python() {
	# Declare an array to define the options of this helper.
	local legacy_args=u
	local -A args_array=( [p]=python= )
	local python
	# Manage arguments with getopts
	ynh_handle_getopts_args "$@"

	# Check python version from APT
	local py_apt_version=$(python3 --version | cut -d ' ' -f 2)

	# Usefull variables
	local python_major=${python%.*}

	# Check existing built version of python in /usr/local/bin
	if [ -e "/usr/local/bin/python$python_major" ]
	then
		local py_built_version=$(/usr/local/bin/python$python_major --version \
			| cut -d ' ' -f 2)
	else
		local py_built_version=0
	fi

	# Compare version
	if $(dpkg --compare-versions $py_apt_version ge $python)
	then
		# APT >= Required
		ynh_print_info --message="Using provided python3..."

		py_app_version="python3"

	else
		# Either python already built or to build
		if $(dpkg --compare-versions $py_built_version ge $python)
		then
			# Built >= Required
			py_app_version="/usr/local/bin/python${py_built_version%.*}"
			ynh_print_info --message="Using already used python3 built version: $py_app_version"
		else
			# APT < Minimal & Actual < Minimal => Build & install Python into /usr/local/bin
			ynh_print_info --message="Building $python (may take a while)..."

			# Store current direcotry
			local MY_DIR=$(pwd)

			# Create a temp direcotry
			tmpdir="$(mktemp --directory)"
			cd "$tmpdir"

			# Download
			wget --output-document="Python-$python.tar.xz" \
				"https://www.python.org/ftp/python/$python/Python-$python.tar.xz" 2>&1

			# Extract
			tar xf "Python-$python.tar.xz"

			# Install
			cd "Python-$python"
			./configure --enable-optimizations
			ynh_exec_warn_less make -j4
			ynh_exec_warn_less make altinstall

			# Go back to working directory
			cd "$MY_DIR"

			# Clean
			ynh_secure_remove "$tmpdir"

			# Set version
			py_app_version="/usr/local/bin/python$python_major"
		fi
	fi
	# Save python version in settings
	ynh_app_setting_set --app=$app --key=python --value="$python"

	# Print some version information:
	ynh_print_info --message="Python version: $($py_app_version -VV)"
	ynh_print_info --message="Pip version: $($py_app_version -m pip -V)"
}
#==================================================================================
#==================================================================================

myynh_setup_python_venv() {
    # Install Python if needed:
    myynh_install_python --python="$py_required_version"

    # Create a virtualenv with python installed by myynh_install_python():
    # Skip pip because of: https://github.com/YunoHost/issues/issues/1960
    ynh_exec_as $app $py_app_version -m venv --clear --upgrade-deps "$data_dir/venv"

	# Print some version information:
	ynh_print_info --message="venv Python version: $($data_dir/venv/bin/python3 -VV)"
	ynh_print_info --message="venv Pip version: $($data_dir/venv/bin/python3 -m pip -V)"

    # run source in a 'sub shell'
    (
        set +o nounset
        source "$data_dir/venv/bin/activate"
        set -o nounset
        set -x
        ynh_exec_as $app $data_dir/venv/bin/pip3 install --upgrade pip wheel setuptools
        ynh_exec_as $app $data_dir/venv/bin/pip3 install --no-deps -r "$data_dir/requirements.txt"
    )
}

myynh_setup_log_file() {
    (
        set -x

        mkdir -p "$(dirname "$log_file")"
        touch "$log_file"

        chown -c -R $app:$app "$log_path"
        chmod -c o-rwx "$log_path"
    )
}

myynh_fix_file_permissions() {
    (
        set -x

        # /var/www/$app/
        chown -c -R "$app:www-data" "$install_dir"
        chmod -c o-rwx "$install_dir"

        # /home/yunohost.app/$app/
        chown -c -R "$app:" "$data_dir"
        chmod -c o-rwx "$data_dir"
    )
}
