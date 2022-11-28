import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import statistics
import math
from scipy import stats


class EbayScraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def website_data(self, search):
        # URL contains search filters: exact match any order, used items, sold listings, and UK only
        url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={search}' \
              f'&_in_kw=4&_ex_kw=&_sacat=0&LH_Sold=1&_udlo=&_udhi=&LH_ItemCondition=4&_samilow=&_samihi=&_stpos=M300AA' \
              f'&_sargn=-1%26saslc%3D1&_fsradio2=%26LH_LocatedIn%3D1&_salic=3&LH_SubLocation=1&_sop=12&_dmd=1&_ipg=60' \
              f'&LH_Complete=1&rt=nc&LH_PrefLoc=1'

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def get_data(self, soup):
        products = []
        results = soup.find('div', {'class': 'srp-river-results clearfix'}).find_all('li', {'class': 's-item '
                                                                                                     's-item__pl-on-bottom'})
        for item in results:
            price = item.find('span', class_='s-item__price').text.replace('£', '').replace(',', '')

            # Removing the results with that show a range of prices for the same listing
            # For example, £169.99 to £189.99
            if 'to' not in price:
                price = float(price)
                products.append(price)

        return products

    def calculate_averages(self, products):
        median = statistics.median(products)
        mode = statistics.mode(products)

        # Mean must be trimmed as some outliers may exist in the search results
        trim_percentage = 0.15
        trimmed_mean = stats.trim_mean(products, trim_percentage)

        return trim_percentage, trimmed_mean, median, mode

    # command to search for sold items on eBay to get an idea of its market value
    @commands.command()
    async def search(self, ctx, *, item):
        if 'help' in item:
            help_embed = discord.Embed(
                title=f'eBay Search Help',
                description='Here are the proper ways to search.\n'
                            'Filters being used: Exact words, Sold listings, Used, UK only',
                colour=0xc48c02,
            )

            help_embed.add_field(name='Format',
                                 value=f'**DO NOT ABUSE** this command as it **may get IP blocked** by eBay!\n'
                                       f'The correct way to search is by typing: !search `[item]`\n\n'
                                       f'Example: !search rtx 3070',
                                 inline=False)
            help_embed.add_field(name='Specific items',
                                 value=f'Items such as CPUs or RAM may get diluted in the search results because '
                                       f'they are part of a PC build. Some items may need to be formatted in a way '
                                       f'so that the search filter searches for the right items.\n\n'
                                       f'Example: !search ryzen 5800x **cpu**\n'
                                       f'Example: !search ddr4 ram **2x8gb**',
                                 inline=False)
            help_embed.add_field(name='0 results',
                                 value=f'You may have entered the wrong spelling of the item you are trying to search '
                                       f'for.\n\n'
                                       f'There may be *no results* for your item on eBay. It might also be because '
                                       f'there are no results with the matching search term.',
                                 inline=False)
            help_embed.add_field(name='What is the trimmed mean?',
                                 value=f'The trimmed mean is the average of the results with the x% of results removed '
                                       f'from the lowest and highest values.\n\n'
                                       f'For this search, the trimmed mean is set to '
                                       f'15%. 15% of the lowest and highest results are removed to remove any '
                                       f'potential outliers.',
                                 inline=False)
            help_embed.add_field(name='Inflated prices',
                                 value=f'If you come across higher/lower values than expected, it may be due to the '
                                       f'search filter being used is accounting for irrelevant items. Even with the '
                                       f'trimmed mean in-place, it cannot remove everything.\n\n'
                                       f'Look at the prices displayed in the Range column. '
                                       f"If the range's lower value is quite low or the range's upper value is quite "
                                       f'high, accessories or other items may be included in the pool of results. ',
                                 inline=False)
            help_embed.add_field(name='Low numbers of items being analysed',
                                 value=f'Sometimes, there are a low number of items being analysed. This is due to '
                                       f'there not being as many items sold on eBay with the search filters being '
                                       f'used. More often, it may mean there is a lack of **used** items being sold.',
                                 inline=False)
            help_embed.add_field(name='If everything fails',
                                 value=f'Please use the manual [eBay Advanced search]'
                                       f'(https://www.ebay.co.uk/sch/ebayadvsearch) and go from there. This bot cannot '
                                       f'help you in this case. :( ',
                                 inline=False)

            await ctx.send(embed=help_embed)

        elif ' ' in item or '' in item:
            # eBay wants to use + in place of spaces in the search term
            formatted_search_term = item.replace(" ", "+")

            soup = self.website_data(formatted_search_term)
            my_list = self.get_data(soup)

            # No items found in search result found and list is empty
            if not my_list:
                no_results_embed = discord.Embed(
                    title=f'eBay Sold Items Search: {item}',
                    description='There were 0 results for your search!',
                    colour=0xce2d32,
                )

                no_results_embed.add_field(name='Wrong spelling?',
                                           value=f'Make sure you spelt the item correctly, as the search filter is '
                                                 f'looking for an exact match. Your search term `{item}` may be '
                                                 f'spelt incorrectly.\n\n'
                                                 f'`!search help` may be able to help you.',
                                           inline=False)
                no_results_embed.add_field(name='No used items being sold with your search term',
                                           value=f'There may be 0 results for your item that are sold as used '
                                                 f'on eBay. Again, the search filter is looking for an exact match for '
                                                 f'the words of the item. \n\n '
                                                 f'Filters being used: Exact words, Sold listings, Used, UK only',
                                           inline=False)
                no_results_embed.add_field(name='Bot no longer working',
                                           value=f'If you know that there are used items in the market and your '
                                                 f'spelling is correct, then the bot may have been IP Blocked by '
                                                 f'eBay.\n\n'
                                                 f'In this case, it might be better for you to manually use the '
                                                 f'[eBay Advanced search](https://www.ebay.co.uk/sch/ebayadvsearch) '
                                                 f'and see the status of the market for your item. This bot cannot '
                                                 f'help you in this situation.',
                                           inline=False)

                await ctx.send(embed=no_results_embed)

            # There are sold items in the search result and the list has values
            else:
                trim_percentage, trimmed_mean, median, mode = self.calculate_averages(my_list)

                # Calculating the total number of results in the list after trimming for the mean
                # Trimming leads to x number of values (rounded up) being removed from both sides of the list
                list_total = len(my_list)

                trimming = list_total * trim_percentage
                trimming = math.ceil(trimming)
                trimmings_for_both_sides = trimming * 2
                trimmed_list_total = list_total - trimmings_for_both_sides

                # Calculating values for the range after trimming
                my_sorted_list = sorted(my_list)

                minimum_value = min(my_sorted_list[trimming:])
                maximum_value = max(my_sorted_list[:-trimming])

                embed = discord.Embed(
                    title=f'eBay Sold Items Search: {item}',
                    description=f'The values below may not contain all of the sold items due to the filers being used '
                                f'on [eBay Advanced search](https://www.ebay.co.uk/sch/ebayadvsearch). The results are '
                                f'trimmed by {int(trim_percentage * 100)}% to remove outliers. Use `!search help` '
                                f'for help.',
                    colour=0x6b9312,
                )

                embed.add_field(name='Average Sold Price', value=f'£{trimmed_mean:.2f}', inline=False)
                embed.add_field(name='Median', value=f'£{median:.2f}', inline=True)
                embed.add_field(name='Mode', value=f'£{mode:.2f}', inline=True)
                embed.add_field(name='Range', value=f'£{minimum_value:.2f} to £{maximum_value:.2f}', inline=True)

                embed.set_thumbnail(
                    url='https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/EBay_logo.svg/2560px-'
                        'EBay_logo.svg.png')
                embed.set_footer(text=f'There were a total of {list_total} search results. After trimming '
                                      f'{trimmings_for_both_sides}, there were {trimmed_list_total} left.',
                                 icon_url='https://img.icons8.com/fluency/512/paid.png')

                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(EbayScraper(bot))
