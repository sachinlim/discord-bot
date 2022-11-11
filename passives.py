# op.gg replaces blank spaces with '%20'
def op_format(summoner_name):
    formatted = summoner_name
    if " " in summoner_name:
        formatted = summoner_name.replace(" ", "%20")

    return formatted


# Both u.gg and Pro Builds removes spaces for web links
def ugg_format(champion_name):
    formatted = champion_name
    if " " in champion_name:
        formatted = champion_name.replace(" ", "")

    return formatted
