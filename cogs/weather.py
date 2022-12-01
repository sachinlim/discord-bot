import discord
from discord.ext import commands
import actives
import datetime
import requests


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_location(self, city):
        """
        Country could also be provided, as a city name can exist in both UK and US
        For example, London exists in Ohio, USA as well
        """
        user_input = city.title()

        if ' ' in city:
            user_input = user_input.split(',')

            input_city = user_input[0]
            input_country = user_input[1].upper()
        else:
            input_city = user_input
            input_country = 'GB'

        return input_city, input_country

    def get_url(self, city, country):
        """
        Calling and formatting the url link for the API
        """
        api_key = actives.weather_api
        units = 'metric'

        url_link = f'https://api.openweathermap.org/data/2.5/weather?q={city}, {country}&appid={api_key}&units={units}'

        return url_link

    def convert_ms_to_mph(self, value):
        """
        This is used to convert m/s to mph for the wind speed
        """
        formula = 2.236936
        ms_to_mph = value * formula

        return ms_to_mph

    def get_thumbnail(self, weather_id):
        """
        Weather conditions to display as thumbnail
        There are different conditions that have their own separate icons with links provided by OpenWeatherMap
        """
        match weather_id:
            case 'Thunderstorm':
                # Group 2xx: Thunderstorm
                condition = '11d'
            case 'Drizzle':
                # Group 3xx: Drizzle
                condition = '09d'
            case 'Rain':
                # Group 5xx: Rain
                condition = '10d'
            case 'Snow':
                # Group 6xx: Snow
                condition = '13d'
            case 'Mist' | 'Smoke' | 'Haze' | 'Dust' | 'Fog' | 'Sand' | 'Ash' | 'Squall' | 'Tornado':
                # Group 7xx: Atmosphere - has 10 separate IDs for Main, but only 9 Main values
                condition = '50d'
            case 'Clear':
                # Group 800: Clear
                condition = '01d'
            case 'Clouds':
                # Group 80x: Clouds
                condition = '04d'
            case _:
                # Default value for conditions that get added in the future
                condition = '01d'

        thumbnail_url = f'http://openweathermap.org/img/wn/{condition}@2x.png'

        return thumbnail_url

    def get_embed_colour(self, number):
        """
        Providing the colour hex values for the embedded message
        Colour depends on the temperature of the location
        """
        if number <= 0:
            return 0xa9d6ea
        if 1 < number <= 10:
            return 0xa9eab0
        if 11 <= number <= 16:
            return 0xb0e07a
        if 17 <= number <= 24:
            return 0xe1c932
        if 25 <= number <= 33:
            return 0xdf4d1c
        if number >= 34:
            return 0xb8001c

    @commands.command()
    async def weather(self, ctx, *, city):
        try:
            city_name, country_code = self.get_location(city)

            url = self.get_url(city_name, country_code)
            response = requests.get(url).json()

            weather_id = response['weather'][0]['main']
            weather_description = response['weather'][0]['description']
            current_temperature = response['main']['temp']
            temperature_feels_like = response['main']['feels_like']
            humidity = response['main']['humidity']
            wind_speed = self.convert_ms_to_mph(response['wind']['speed'])

            sunrise_time = datetime.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

            temperature = self.get_embed_colour(current_temperature)

            embed = discord.Embed(
                title=f'Weather Update',
                colour=temperature,
            )

            embed.set_thumbnail(url=self.get_thumbnail(weather_id))

            embed.add_field(name=f'{city_name}, {country_code}',
                            value=f'**Conditions**: {weather_description.title()}\n'
                                  f'**Temperature**: {current_temperature}°C\n'
                                  f'**Feels like**: {temperature_feels_like}°C\n'
                                  f'**Humidity**: {humidity}%\n'
                                  f'**Wind Speed**: {wind_speed:.2f} mph',
                            inline=False)

            embed.set_footer(text=f'Sunrise is at {sunrise_time:%H:%M} am and Sunset is at {sunset_time:%H:%M} pm '
                                  f'local time | OpenWeatherMap',
                             icon_url='https://openweathermap.org/themes/openweathermap/assets/img/mobile_app'
                                      '/android-app-top-banner.png')

            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(
                title="No response",
                color=0xce2d32)

            embed.add_field(name='Error',
                            value='Please enter a a valid city and check its 2-digit country code '
                                  'if it is not in the UK.',
                            inline=True)

            embed.set_footer(text=f'OpenWeatherMap',
                             icon_url='https://openweathermap.org/themes/openweathermap/assets/img/mobile_app'
                                      '/android-app-top-banner.png')

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Weather(bot))
