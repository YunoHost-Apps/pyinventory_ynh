#!/bin/bash

#=================================================
# RETRIEVE ARGUMENTS FROM THE MANIFEST
#=================================================

domain=$YNH_APP_ARG_DOMAIN
path_url=$YNH_APP_ARG_PATH
admin=$YNH_APP_ARG_ADMIN
is_public=$YNH_APP_ARG_IS_PUBLIC
app=$YNH_APP_INSTANCE_NAME

#=================================================
# SET CONSTANTS
#=================================================

public_path=/var/www/$app
final_path=/opt/yunohost/$app
log_path=/var/log/$app
log_file="${log_path}/pyinventory.log"

#=================================================
# COMMON VARIABLES
#=================================================

# dependencies used by the app
pkg_dependencies="build-essential python3-dev python3-pip python3-virtualenv virtualenv git \
	postgresql postgresql-contrib"

# PyInventory's version for PIP and settings file
pyinventory_version="0.8.1rc2"


#=================================================
# Redis HELPERS
#=================================================

# get the first available redis database
#
# usage: ynh_redis_get_free_db
# | returns: the database number to use
ynh_redis_get_free_db() {
	local result max db
	result=$(redis-cli INFO keyspace)

	# get the num
	max=$(cat /etc/redis/redis.conf | grep ^databases | grep -Eow "[0-9]+")

	db=0
	# default Debian setting is 15 databases
	for i in $(seq 0 "$max")
	do
	 	if ! echo "$result" | grep -q "db$i"
	 	then
			db=$i
	 		break 1
 		fi
 		db=-1
	done

	test "$db" -eq -1 && ynh_die "No available Redis databases..."

	echo "$db"
}

# Create a master password and set up global settings
# Please always call this script in install and restore scripts
#
# usage: ynh_redis_remove_db database
# | arg: database - the database to erase
ynh_redis_remove_db() {
	local db=$1
	redis-cli -n "$db" flushall
}