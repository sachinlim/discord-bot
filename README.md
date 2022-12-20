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

For MacOS, `pip3` might need to be used.
```
# Installing the entire requirements.txt file
pip3 install -r requirements.txt

# Manual installation of modules
pip3 install discord, selenium, requests, beautifulsoup4
```


In order for the [op.gg](https://www.op.gg/) Live Game scraper to work, [ChromeDriver](https://chromedriver.chromium.org/downloads) needs to be downloaded and placed in the same directory as the [dukies-bot.py](dukies-bot.py) file.


## Screenshots


### eBay scraper

This is the `!search` command that provides information from [eBay's advance search](https://www.ebay.co.uk/sch/ebayadvsearch) by scraping the information available. It uses Beautiful Soup to scrape the information while using the filters: Exact words, any order, Sold listings, Used, UK only.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208089922-d21f70c6-e779-4371-9c84-28a00093a3ea.JPG">
</p>

Sometimes, items are sold in bulk in a single listing, such as "5x Intel i5-7400", meaning the price for the listing is 5 times higher than if it was a single item sold. To try and avoid abnormalities like these, trimming is done by 15% from the lowest and highest prices, reducing the total list of items down to 70%. This should mean that most of the outliers are removed.

In the event that there is a typo in the search term or the item does not exist, an error message is sent: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208090929-065cead7-6951-41d9-bf64-3519e189e7c7.JPG">
</p>

### op.gg Live Game scraper 

This scraper was made using Selenium to have information scraped. There are two versions of this: one using the command `!ig` which only provides the URL for the specified account name, while `!ig2` provides the scraped information. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208095857-7d77e066-b103-48f1-8621-e5cadd57b82c.JPG">
</p>

As op.gg uses Javascript to display information from the Riot API, it requires the use of Javascript to be enabed. This meant that Beautiful Soup would not work, therefore, Selenium was used alongside ChromeDriver. 

The UI for op.gg's Live Game looks like this: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208096006-287f7a3e-acf2-4d79-bf9e-a2f94f2467d2.JPG">
</p>

Discord's embedded messages have a limit of only displaying 3 rows, therefore, only 3 sets of information could be included. This is fine, as the useful information that is needed are: Champion (character) name, rank, and win rate.


### Weather

This below is the hourly weather update. It can also be called manually with the `!weather` command with the location also entered.

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208090106-aa67e793-48e0-4b29-8325-60a34a09cb79.JPG">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208090697-57ac805c-b9a3-4675-adf7-45fc6e7b72bb.JPG">
</p>

### Link Shortener

This is available for UK eBay and Amazon links. These websites only need the item number to show the correct listing but there are many occasions where other information is added onto the website URL. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208097028-22ee0a97-5b46-4d91-a4a0-26880d1e1095.JPG">
</p>

The original URL could be something like: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/208101547-44e473bf-8c1a-4b99-b484-c8d3f084dc34.JPG">
</p>
