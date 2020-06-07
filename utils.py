import fileinput
import os
import secrets

def handle_installed_apps(filepath, settings_dict):
    with fileinput.input(filepath, inplace=True) as f:
        is_installed_apps = False
        for line in f:
            if 'INSTALLED_APPS' in line:
                is_installed_apps = True
            if is_installed_apps and ']' in line:
                is_installed_apps = False
                for app in settings_dict['add']:
                    print(f'\t\'{app}\',\n', end='')
            print(line, end='')


def set_up_environ(filepath):
    env_vars = {}
    with fileinput.input(filepath, inplace=True) as f:
        for line in f:
            if 'import os' in line:
                print(line, end='')
                print('import environ')
                print('\n')
                print('env = environ.Env(\n\tDEBUG=(bool,False),\n\tALLOWED_HOSTS=(list,["*"])\n)')
                print('environ.Env.read_env("../.env")')
                continue
            if 'SECRET_KEY' in line:
                env_vars['SECRET_KEY'] = line[line.find('\''):][1:-2]
                print('SECRET_KEY=env.str("SECRET_KEY")')
                continue
            if 'DEBUG' in line:
                env_vars['DEBUG'] = 'True'
                print('DEBUG=env.bool("DEBUG")')
                continue
            if 'ALLOWED_HOSTS' in line:
                env_vars['ALLOWED_HOSTS'] = '*'
                print('ALLOWED_HOSTS=env.list("ALLOWED_HOSTS")')
                continue
            print(line, end='')
    return env_vars


def add_static_root(filepath):
    with open(filepath, mode='a') as f:
        f.write('STATIC_ROOT = os.path.join(BASE_DIR, "static_col")')


def edit_django_settings(filepath, settings_dict):
    env_vars = {}
    if settings_dict['set_up_environ']:
        env_vars = set_up_environ(filepath)
    if settings_dict['static_root']:
        add_static_root(filepath)
    if 'INSTALLED_APPS' in settings_dict:
        handle_installed_apps(filepath, settings_dict['INSTALLED_APPS'])
    return env_vars


def edit_packagejson(filepath, settings_dict):
    with fileinput.input(filepath, inplace=True) as f:
        is_scripts = False
        for line in f:
            if 'scripts' in line:
                is_scripts = True
                print(line, end='')
                for script in settings_dict['scripts']['replace']:
                    print(f'\t\t\"{script["name"]}\":\"{script["command"]}\",\n', end='')
                continue
            if is_scripts and '}' in line:
                is_scripts = False
            print(line, end='')


def get_postgresql_url(**kwargs):
    return f'postgres://{kwargs["username"]}:{kwargs["password"]}@{kwargs["address"]}:{kwargs["port"]}/{kwargs["name"]}'

def get_sqlite_url(path):
    return f'sqlite:///{path}.db'

def get_django_secret_key():
    return secrets.token_urlsafe(50)
