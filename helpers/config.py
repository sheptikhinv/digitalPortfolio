from configparser import ConfigParser

config = ConfigParser()


def get_value(key: str) -> str:
    try:
        file = open("settings.ini", "x")
        file.close()
    except FileExistsError:
        pass

    config.read("settings.ini")
    try:
        value = config["SETTINGS"][key]
    except KeyError:
        value = input(f"Enter {key}: ")
        if not config.has_section("SETTINGS"):
            config.add_section("SETTINGS")
        config.set("SETTINGS", key, value)
        with open("settings.ini", "w") as configfile:
            config.write(configfile)

    return value
