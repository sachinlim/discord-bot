<img align="right" src="https://cdn-icons-png.flaticon.com/512/4233/4233830.png" width="100">
<img align="right" src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/625e5fcef7ab80b8c1fe559e_Discord-Logo-Color.png" width="90">

# Discord Bot 

Discord bot designed to keep servers clean with shortening long links and adding commands to help reduce search times. 

It is made with [Discord.py](https://discordpy.readthedocs.io/en/stable/) API, and with how the API works, it allows the ability to store features for the bot in a separate class with the use of the [Discord.py cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) feature. The features of this Bot can be found in the [cogs](cogs) directory. 

## Key Features

* [eBay](https://www.ebay.co.uk/) sold price scraper for used items
* [op.gg](https://www.op.gg/) Live Game scraper
* Weather updates
* Link shortener for eBay and Amazon

These features found in the [cogs](cogs) directory can be extracted and implemented in another Python script as long as the relevant modules are installed. For example, the [eBay scraper](cogs/eBay.py) is a variant of the [ebay-sold-prices](https://github.com/sachinlim/ebay-sold-prices) project. 

## Prerequisites

The Bot is created using Python 3.10 and requires a few modules to be installed. 

Installing using `pip`

```
# Installing the entire requirements.txt file
pip install -r requirements.txt

# Manual installation of modules
pip install discord, selenium, requests, beautifulsoup4
```

For MacOS, `pip3` might need to be used
```
# Installing the entire requirements.txt file
pip3 install -r requirements.txt

# Manual installation of modules
pip3 install discord, selenium, requests, beautifulsoup4
```


In order for the [op.gg](https://www.op.gg/) Live Game scraper to work, [ChromeDriver](https://chromedriver.chromium.org/downloads) needs to be downloaded and placed in the same directory as the [dukies-bot.py](dukies-bot.py) file.


## Screenshots


### eBay scraper

This is the `!search` command that provides information from [eBay's advance search](https://www.ebay.co.uk/sch/ebayadvsearch) by scraping the information available. It uses Beautiful Soup to scrape the sold prices while using the filters: Exact words, any order, Sold listings, Used, UK only. The prices are stored in a list before the Bot is able to present information to the user regarding the value of the item in the current market.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208790787-ef499007-b8bd-4b16-9b9a-0dfce2b813be.png" width="550">
</p>

Sometimes, the description of a listing can tell potential buyers that an item is faulty. Other times, the items are sold in bulk in a single listing, such as "5x Intel i5-7400", meaning the price for the listing is 5 times higher than if it was a single item being sold. To try and avoid abnormalities like these, data trimming is done by 15% for the lowest and highest prices, which reduces the total list of items down to 70%. This should mean that most of the outliers are removed.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208791107-109466a1-0bfc-46c4-b073-5235a69afc91.png" width="550">
</p>


In the event that there is a typo in the search term or the item does not exist, an error message is sent, like the one above.
### op.gg Live Game scraper 

This scraper was made using Selenium to have information scraped. There are two versions of this: one using the command `!ig` which only provides the URL for the specified account name, while `!ig2` provides the scraped information. 


The UI for op.gg's Live Game looks like this: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208790049-5a7aa954-7d74-448e-a297-34ab69722487.png">
</p>

As op.gg uses Javascript to display information from the Riot API, it requires the use of Javascript to be enabed. This meant that Beautiful Soup would not work, therefore, Selenium was used alongside ChromeDriver. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208790537-bfd142cc-5303-4df7-b56d-eb708d09d688.png" width="550">
</p>

Discord's embedded messages have a limit of only displaying 3 rows, therefore, only 3 sets of information could be included. This is fine, as the useful information that is needed are: Champion (character) name, rank, and win rate.



### Weather

This below is the hourly weather update. It can also be called manually with the `!weather` command with the location also entered. The JSON data for the relevant city is called using the [Weather API](https://openweathermap.org/current) from [OpenWeatherMap](https://openweathermap.org/), and formatted to fit Discord's embedded messages.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208791723-9bf20d23-30ef-49f6-9eee-75a5a9f08582.png" width="500">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208792049-bf1a4637-5df3-448d-a2e1-086b9dfe4066.png" width="500">
</p>

### Link Shortener

This is available for UK eBay and Amazon links. These websites only need the item number to show the correct listing but there are many occasions where other information is added onto the website URL. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208792182-cfd2e36b-69bd-462f-8e60-d8ee54375174.png" width="800">
</p>

The original URL could be something like: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208792316-35c89c0e-d495-4f6f-a55e-185e62a6669c.png" width="900">
</p>

