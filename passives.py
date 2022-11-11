
def op_format(summoner_name):
    formatted = summoner_name
    if " " in summoner_name:
        formatted = summoner_name.replace(" ", "%20")

    return formatted


