from selenium import webdriver
from selenium.webdriver.common.by import By


def get_data(summoner_name):
    url = f'https://www.op.gg/summoners/euw/{summoner_name}/ingame'

    path = 'chromedriver'
    driver = webdriver.Chrome(path)
    driver.get(url)

    summoners = []
    ranks = []
    win_rates = []

    summoner_name = driver.find_elements(By.XPATH, '//td[1]/a/div/img')
    for summoner in summoner_name:
        champ = summoner.get_attribute('alt')
        summoners.append(champ)

    current_rank = driver.find_elements(By.CLASS_NAME, 'current-rank')
    for rank in current_rank:
        formatted = rank.text.replace('(', ' (')
        ranks.append(formatted)

    winratio = driver.find_elements(By.XPATH, '//td[7]')
    for ratios in winratio:
        win_rates.append(ratios.text)

    final_list = list(zip(summoners, ranks, win_rates))

    driver.quit()
    return final_list
