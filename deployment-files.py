import os
import chevron

'''
set up deployment files for the specific app
- gunicorn start
- nginx config file
- systemd for gunicorn process
'''

MASTER_FILES_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'master_files',
    'deployment-files'
)

app_name = input("App name: ")
app_user = input("System user: ")
app_dir = input("App directory: ")
app_url = input("App URL: ")

config_dict = {
        'app_name': app_name,
        'app_user': app_user,
        'app_dir': app_dir,
        'app_url': app_url,
    }

with open(os.path.join(MASTER_FILES_PATH, "gunicorn_start.template"), "r") as f:
    rendered = chevron.render(f, config_dict)
    with open('gunicorn_start', 'w') as gf:
        gf.write(rendered)


with open(os.path.join(MASTER_FILES_PATH, "nginx_config.template"), "r") as f:
    rendered = chevron.render(f, config_dict)
    with open(f'{config_dict["app_name"]}', 'w') as nginxf:
        nginxf.write(rendered)

with open(os.path.join(MASTER_FILES_PATH, "systemd.template"), "r") as f:
    rendered = chevron.render(f, config_dict)
    with open(f'{config_dict["app_name"]}.service', 'w') as systemdf:
        systemdf.write(rendered)