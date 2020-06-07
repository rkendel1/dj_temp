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


def make_files(app_name, app_url, location_path):
    config_dict = {
            'app_name': app_name,
            'app_user': app_name,
            'app_dir': app_name,
            'app_url': app_url,
        }

    os.chdir(location_path)
    files = {
        'gunicorn_start': 'gunicorn_start',
        'nginx_conf': f'{config_dict["app_name"]}',
        'systemd_service': f'{config_dict["app_name"]}.service',
    }

    with open(os.path.join(MASTER_FILES_PATH, "gunicorn_start.template"), "r") as f:
        rendered = chevron.render(f, config_dict)
        with open(files['gunicorn_start'], 'w') as gf:
            gf.write(rendered)
            files['gunicorn_start'] = os.path.realpath(files['gunicorn_start'])


    with open(os.path.join(MASTER_FILES_PATH, "nginx_config.template"), "r") as f:
        rendered = chevron.render(f, config_dict)
        with open(f'{config_dict["app_name"]}', 'w') as nginxf:
            nginxf.write(rendered)
            files['nginx_conf'] = os.path.realpath(files['nginx_conf'])

    with open(os.path.join(MASTER_FILES_PATH, "systemd.template"), "r") as f:
        rendered = chevron.render(f, config_dict)
        with open(files['systemd_service'], 'w') as systemdf:
            systemdf.write(rendered)
            files['systemd_service'] = os.path.realpath(files['systemd_service'])

    #todo make .env file
    return files