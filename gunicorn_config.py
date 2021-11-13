command = '/home/django/proj/venv_ie/bin/gunicorn'
pythonpath = '/home/django/proj/intergalactic'
bind = '127.0.0.1:8001'
workers = 3
user = 'django'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=intergalactic.settings'
