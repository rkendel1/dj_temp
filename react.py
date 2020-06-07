#!./venv/bin/python
import os
import platform
from shutil import copyfile, copytree
import subprocess
from utils import edit_django_settings, edit_packagejson
import master_files

MASTER_FILES_PATH = os.path.join(
    os.path.dirname(master_files.__file__),
    'react'
)

PROJECT_NAME = input('Project name: ')
VENV_NAME = 'venv'
REQUIREMENTS_FILE = 'requirements.txt'
CWD_PATH = os.getcwd()

DEFAULT_APP_NAME = 'app'
DEFAULT_FRONTEND_APP_NAME = 'frontend'

if platform.system() == 'Linux':
    SCRIPTS_PATH = 'bin'
    SCRIPTS_SUFFIX = ''
elif platform.system() == 'Windows':
    SCRIPTS_PATH = 'Scripts'
    SCRIPTS_SUFFIX = '.exe'

VENV_BIN_PATH = f"{VENV_NAME}/{SCRIPTS_PATH}"

'''
+++ folder structure
1. make new folder named project_name

project_name
++ venv
++ node_modules
++ app (django installed here)
    ++ frontend
    ++ project_name
    ++ templates
    -- manage.py
-- requirements.txt
-- .gitignore
-- package.json
-- .babelrc
-- webpack.config.js
'''

os.mkdir(os.path.join(CWD_PATH, PROJECT_NAME))
CWD_PATH = os.path.join(CWD_PATH, PROJECT_NAME)
os.chdir(CWD_PATH)

'''

+++ django set up
2. make virtual env called venv
3. make requirements.file
4. pip install from requirements file
5. install django to ./app folder
5. set up django-environ
6. start frontend app
7. add django-rest, frontend to INSTALLED_APPS

'''

copyfile(
    os.path.join(MASTER_FILES_PATH, 'requirements.txt'),
    os.path.join(CWD_PATH, REQUIREMENTS_FILE),
)
os.system(f'virtualenv {VENV_NAME}')
subprocess.call([
    os.path.join(CWD_PATH, f'{VENV_BIN_PATH}/pip{SCRIPTS_SUFFIX}'),
    'install', '-r', REQUIREMENTS_FILE
])

subprocess.call([
    os.path.join(CWD_PATH, f'{VENV_BIN_PATH}/django-admin{SCRIPTS_SUFFIX}'),
    'startproject', DEFAULT_APP_NAME
])
os.chdir(os.path.join(CWD_PATH, DEFAULT_APP_NAME))
subprocess.call([
    os.path.join(CWD_PATH, f'{VENV_BIN_PATH}/django-admin{SCRIPTS_SUFFIX}'),
    'startapp', DEFAULT_FRONTEND_APP_NAME
])

# add django-rest to installed apps
settings_file_path = os.path.join(CWD_PATH, DEFAULT_APP_NAME, DEFAULT_APP_NAME, 'settings.py')
env_vars = edit_django_settings(settings_file_path, {
    'set_up_environ': True,
    'static_root': True,
    'INSTALLED_APPS': {
        'add': [
            'rest_framework',
            'frontend',
        ]
    }
})

#create .env file
with open(os.path.join(CWD_PATH,'.env'), 'w') as file:
    for var,value in env_vars.items():
        file.write(
            f'{var}={value}\n'
        )

# add view, urls.py and template, static, src
copytree(
    os.path.join(MASTER_FILES_PATH, 'django', 'frontend', 'src'),
    os.path.join(CWD_PATH, 'app', 'frontend', 'src')
)
copytree(
    os.path.join(MASTER_FILES_PATH, 'django', 'frontend', 'static'),
    os.path.join(CWD_PATH, 'app', 'frontend', 'static')
)
copytree(
    os.path.join(MASTER_FILES_PATH, 'django', 'frontend', 'templates'),
    os.path.join(CWD_PATH, 'app', 'frontend', 'templates')
)
copyfile(
    os.path.join(MASTER_FILES_PATH, 'django', 'app', 'urls.py'),
    os.path.join(CWD_PATH, 'app', 'app', 'urls.py'),
)
copyfile(
    os.path.join(MASTER_FILES_PATH, 'django', 'frontend', 'urls.py'),
    os.path.join(CWD_PATH, 'app', 'frontend', 'urls.py'),
)
copyfile(
    os.path.join(MASTER_FILES_PATH, 'django', 'frontend', 'views.py'),
    os.path.join(CWD_PATH, 'app', 'frontend', 'views.py'),
)
'''

+++ javascript set up
1. run npm init -y
2. install babel, webpack, reactjs
3. edit package.json, babel.rc, webpack.config.js
'''
os.chdir(CWD_PATH)
os.system('npm init -y')
os.system('npm i webpack webpack-cli --save-dev')
os.system(
    'npm i @babel/core babel-loader @babel/preset-env @babel/preset-react babel-plugin-transform-class-properties @babel/plugin-transform-runtime --save-dev')
os.system('npm i react react-dom prop-types --save-dev')

# add scripts to package.json
packagejson_file_path = os.path.join(CWD_PATH, 'package.json')
edit_packagejson(
    packagejson_file_path,
    {
        'scripts': {
            'replace': [
                {'name': 'dev', 'command': "webpack --mode development"},
                {'name': 'prod', 'command': "webpack --mode production"},
            ]
        }
    }
)

copyfile(
    os.path.join(MASTER_FILES_PATH, '.babelrc'),
    os.path.join(CWD_PATH, '.babelrc'),
)
copyfile(
    os.path.join(MASTER_FILES_PATH, 'webpack.config.js'),
    os.path.join(CWD_PATH, 'webpack.config.js'),
)

'''

+++ simple app
1. run compile js command

100. create .gitignore and run git init, git add *, git commit "initial commit"
'''
os.system('npm run dev')

copyfile(
    os.path.join(MASTER_FILES_PATH, '.gitignore'),
    os.path.join(CWD_PATH, '.gitignore'),
)
os.system('git init')
os.system('git add *')
os.system('git commit -m "initial commit"')
