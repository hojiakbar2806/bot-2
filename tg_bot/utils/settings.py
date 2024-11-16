import json


settings_path: str = "./data/settings.json"


def parse_settings():
    with open(settings_path, "r") as file:
        return json.loads(file.read())


def change_settings(section: str, new_value, _name=None, _active=None):
    settings = parse_settings()

    with open(settings_path, "w") as file:
        if _name is not None:
            if _active is not None:
                settings[section][_name][_active] = new_value
            else:
                settings[section][_name] = new_value
        else:
            settings[section] = new_value
        json.dump(settings, file, indent=4)

    return settings
