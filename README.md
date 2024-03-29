<img align="right" src="https://cdn-icons-png.flaticon.com/512/4233/4233830.png" width="100">
<img align="right" src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/625e5fcef7ab80b8c1fe559e_Discord-Logo-Color.png" width="90">

# Discord Bot 

Discord bot designed to keep servers clean with shortening long links and adding commands to help reduce search times.

It is made with [Discord.py](https://discordpy.readthedocs.io/en/stable/) API wrapper, and with how the API wrapper works, it allows the ability to store features for the bot in a separate class with the use of the [Discord.py cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) feature. The features of this Bot can be found in the [cogs](cogs) directory. 

### Additional Bots

As this was the first venture with creating bots, other Discord bots have also been created, which adopt certain [cogs](cogs) and include new ones. The other bots seeing the most use is the [hwsuk-bot](https://github.com/sachinlim/hwsuk-bot), which was created for a community of 19,000 hardware traders on Reddit, located in the UK. The bot is available to a growing community of 2000 users that are involved in the community's Discord server.   

## Key Features

* [eBay](https://www.ebay.co.uk/) sold price scraper for used items
* [op.gg](https://www.op.gg/) Live Game scraper
* Weather updates
* Link shortener for eBay and Amazon

These features found in the [cogs](cogs) directory can be extracted and implemented as a standalone Python script, as long as the relevant modules are installed. This allows for the use of Discord bots to act as a wrapper that impements many projects as commands.

## Prerequisites

The Bot is created using Python 3.10 and requires a few modules to be installed. 

Installing using `pip`

```
# Installing the entire requirements.txt file
pip install -r requirements.txt

# Manual installation of modules
pip install discord selenium requests beautifulsoup4
```

In order for the [op.gg](https://www.op.gg/) Live Game scraper to work, [ChromeDriver](https://chromedriver.chromium.org/downloads) needs to be downloaded and placed in the same directory as the [dukies-bot.py](dukies-bot.py) file. There should be another file called `actives.py`, where the bot can get private variables from, such as the token ID for the bot or the channel IDs for the hourly weather updates.

### Staying online

To host this on DigitalOcean (or any cloud provider), GNU screen has been used to always keep the bot online. If you run the bot script with `python3 dukies-bot.py`, it will no longer be online after you close the console/terminal. To prevent this and always stay online, screen can be used.

* Install screen `pip install screen`
* Write `screen` to open it up
* Read the message and press enter
* Navigate to your script and run it with `python3 dukies-bot.py`
* Close the window or exit screen with `[CTRL] + A + D`

One thing I discovered was that the basic Droplet on DigitalOcean was not good enough for [hwsuk-bot](https://github.com/sachinlim/hwsuk-bot) because the screen instance would kill itself after a few days. After looking at the activity history on DigitalOcean, there were random CPU spikes, over 70% memory utilisation, and high disk usage. This made me upgrade one tier up, to a Droplet with 1GB RAM but still with one CPU core. There have been no issues so far.


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
  <img src="https://user-images.githubusercontent.com/80691974/212424494-8d10f5f4-37f8-4580-9647-a8f34bb7a91b.png" width="650">
</p>


The original URL could be something like: 

<p align="center">
  <img src="https://user-images.githubusercontent.com/80691974/212424589-70798d6d-2de6-4583-a8a4-ab3c58e31123.png" width="650">
</p>

