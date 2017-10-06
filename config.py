import configparser
import os


def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Player_Settings")
    config.add_section("Game")
    config.add_section("Archers")
    config.add_section("Magic")
    config.add_section("Poison")
    config.add_section("Tree")
    config.add_section("Dragon")
    config.add_section("Skeleton")

    config.set("Player_Settings", "gold", "130")
    config.set("Player_Settings", "level_reward", "250")
    config.set("Player_Settings", "health", "20")

    config.set("Game", "mag_price", "25")
    config.set("Game", "poi_price", "30")
    config.set("Game", "castle_1", "50")
    config.set("Game", "castle_2", "75")
    config.set("Game", "lvl_up_healing_1", "12")
    config.set("Game", "lvl_up_healing_2", "10")

    config.set("Archers", "speed", "15")

    config.set("Archers", "damage_1", "25")
    config.set("Archers", "range_1", "500")
    config.set("Archers", "price", "15")
    config.set("Archers", "lvl_up", "20")
    config.set("Archers", "attack_speed_1", "100")

    config.set("Archers", "damage_2", "35")
    config.set("Archers", "range_2", "550")
    config.set("Archers", "attack_speed_2", "50")

    config.set("Archers", "damage_3", "45")
    config.set("Archers", "range_3", "600")
    config.set("Archers", "attack_speed_3", "25")

    config.set("Magic", "speed", "10")
    config.set("Magic", "pounce_range", "200")

    config.set("Magic", "damage_1", "20")
    config.set("Magic", "pounce", "3")
    config.set("Magic", "range_1", "400")
    config.set("Magic", "price", "25")
    config.set("Magic", "lvl_up", "15")
    config.set("Magic", "attack_speed_1", "100")

    config.set("Magic", "damage_2", "30")
    config.set("Magic", "range_2", "450")
    config.set("Magic", "attack_speed_2", "50")
    config.set("Magic", "damage_3", "40")
    config.set("Magic", "range_3", "500")
    config.set("Magic", "attack_speed_3", "25")

    config.set("Poison", "speed", "9")

    config.set("Poison", "damage_1", "20")
    config.set("Poison", "pounce", "3")
    config.set("Poison", "range_1", "300")
    config.set("Poison", "price", "20")
    config.set("Poison", "lvl_up", "15")
    config.set("Poison", "attack_speed_1", "125")
    config.set("Poison", "slow_1", "0.5")

    config.set("Poison", "damage_2", "30")
    config.set("Poison", "range_2", "400")
    config.set("Poison", "attack_speed_2", "100")
    config.set("Poison", "slow_2", "0.7")

    config.set("Poison", "damage_3", "40")
    config.set("Poison", "range_3", "450")
    config.set("Poison", "attack_speed_3", "75")
    config.set("Poison", "slow_3", "0.9")

    config.set("Tree", "damage", "1")
    config.set("Tree", "health", "100")
    config.set("Tree", "speed", "3")
    config.set("Tree", "range_1", "5")
    config.set("Tree", "range_2", "200")
    config.set("Tree", "animation", "16")

    config.set("Tree", "price", "5")
    config.set("Tree", "hitbox", "10")

    config.set("Dragon", "damage", "1")
    config.set("Dragon", "health", "1000")
    config.set("Dragon", "speed", "3")
    config.set("Dragon", "range_1", "15")
    config.set("Dragon", "range_2", "200")
    config.set("Dragon", "price", "30")
    config.set("Dragon", "hitbox", "10")

    config.set("Skeleton", "damage", "1")
    config.set("Skeleton", "health", "80")
    config.set("Skeleton", "speed", "5")
    config.set("Skeleton", "range_1", "5")
    config.set("Skeleton", "range_2", "200")
    config.set("Skeleton", "price", "30")
    config.set("Skeleton", "hitbox", "10")
    config.set("Skeleton", "animation", "36")


    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )

    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)

