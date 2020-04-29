import fileinput


def edit_django_settings(filepath, settings_dict):
    with fileinput.input(filepath, inplace=True) as f:
        is_installed_apps = False
        for line in f:
            if 'INSTALLED_APPS' in line:
                is_installed_apps = True
            if is_installed_apps and ']' in line:
                is_installed_apps = False
                for app in settings_dict['INSTALLED_APPS']['add']:
                    print(f'\t\'{app}\',\n', end='')
            print(line, end='')


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