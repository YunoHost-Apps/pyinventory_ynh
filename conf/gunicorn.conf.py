"""
    Configuration for Gunicorn
"""
import multiprocessing


bind = '127.0.0.1:__PORT__'

# https://docs.gunicorn.org/en/latest/settings.html#workers
workers = multiprocessing.cpu_count() * 2 + 1

# https://docs.gunicorn.org/en/latest/settings.html#logging
loglevel = 'info'

# https://docs.gunicorn.org/en/latest/settings.html#syslog
syslog = True

# https://docs.gunicorn.org/en/latest/settings.html#pidfile
pidfile = '__FINAL_HOME_PATH__/gunicorn.pid'
