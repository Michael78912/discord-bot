import pprint
import time as _time
import traceback
import os
import shutil
import string
import random
import json
import socket
import sys

if socket.gethostname() == 'Michael':
    os.chdir(os.path.dirname(__file__))
    class process:
        class env:
            TOKEN = open(os.path.join(os.getcwd(), '../p')).read()


from pytemperature import k2f, k2c
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen
import wikipedia
import pyowm

from stdabsorb import StdAbsorber

bot = commands.Bot(command_prefix=">", description='A bot that does absolutely nothing useful.')
client = discord.Client()

BAD_COMMANDS = ['os.system', 'os.chdir', 'os.listdir', 'os.remove', 'import shutil',
                '__import__(\'shutil\')', 'exit', 'Exit', 'quit', 'KeyboardInterrupt']

@bot.command()
async def snowman(ctx):
    """
    send a snowman
    """
    await ctx.send("lol you expected, a snowman, but i can't do that, so have an 8.")


@bot.command()
async def mention(ctx, do_it='yes'):
    """
    mention the sender
    if do_it == 'yes': actually do it.
    """
    if do_it == 'yes':
        await ctx.send(ctx.author.mention)

@bot.command()
async def time_in_kelowna(ctx):
    """
    send the current time in Kelowna, BC, Canada.
    """
    await ctx.send(_time.asctime())

@bot.command()
async def see_kelowna(ctx, option='--embed'):
    """
    send a picture of the current view of kelowna, BC Canada.

    >see_kelowna --url: sends the link to the image instead of embeding an actual file
    >see_kelowna --embed / >see_kelowna: embeds the file
    """
    soup = BeautifulSoup(urlopen('https://www.castanet.net/scenic-web-cams/camera/7/', ))
    division = soup.find('img', {'id': 'camImage', 'alt': 'Downtown Kelowna'})
    img_url = division.get_attribute_list('src')[0]
    channel = ctx.channel
    if option == '--url':
        await ctx.send('image of kelowna: ' + img_url)
        print(img_url)

    elif option == '--embed':
        with open('kelowna.png', 'wb') as f:
            shutil.copyfileobj(urlopen(img_url), f)
        await channel.send(file=discord.File('kelowna.png'))

@bot.command()
async def wiki_summary(ctx, item):
    """
    search wikipedia for item and output summary.
    if no item is found, will output "no summary for [item] found"
    """
    try:
        await ctx.send(wikipedia.summary(item))
    except:
        await ctx.send("no summary found for %a found." % item)
            

class Joker:
    def __init__(self):
        parser = BeautifulSoup(
            urlopen('https://michael78912.github.io/puns.html'))
        self.division = parser.p.get_text().split('\n')[2:-1]
        self.joke = random.choice(self.division).strip()

    def say_joke(self):
        print(self.joke)

    def new_joke(self):
        self.joke = random.choice(self.division)



@bot.command()
async def utf8_char(ctx, code):
    """
    outputs the unicode of code
    also accepts a range, ex: >utf8_char 0-10 will output chars 0 - 10.
    """
    try:
        if '-' in code:
            codes = code.split('-')
            new = []
            for i in codes:
                new.append(i.strip())
                print(new)
            codes = [int(i) for i in new]
            iterable = range(*codes)

        else:
            iterable = [int(code)]

    except:
        await ctx.send('invalid number/range')
        raise
        return

    contents = ''
    for i, x in zip(iterable, range(len(iterable))):
        contents += '%d: %s, ' % (x, chr(i))
    await ctx.send(contents)


@bot.command()
async def python_exec(ctx, *, code):
    """
    executes python code, and outputs as a message.
    feel free to use code blocks for multiple lines.
    ONLY USE SINGLE QUOTES: if you MUST use a double quote, escape it with a backslash.
    spaces are accepted.
    """
    print(code)

    code = code.strip('`')
    if code.startswith('python\n'):
        code = '\n'.join(code.split('\n')[1:])
    for cmd in BAD_COMMANDS:
        if cmd in code:
            await ctx.send(ctx.author.mention + ' I can\'t let you execute %a, for the health of my own\
computer. this is because you could do something on MY computer that I don\'t want you to do' % code)
            return
    
    stdout = StdAbsorber('stdout')
    stdout.set_file()
    try:
        exec(code)
        return_str = stdout.read()
        stdout.reset()

    except Exception as e:
        stdout.reset()
        return_str = get_details(e)
        print(return_str)

    return_str = '```' + return_str + '```' if return_str != '' else 'No output'


    await ctx.send(return_str)

@bot.command()
async def get_weather(ctx, city, country):
    """
    sends the weather for city, country.
    also sends an icon of the weather.
    """
    city = city.lower().strip().title()
    country = country.lower().strip().title()
    owm = pyowm.OWM('5949da28441858d0fcb6070f3cbf6836')
    try:
        weather_json = json.loads(owm.weather_at_place('{},{}'.format(city, country)).to_JSON())['Weather']
    except:
        await ctx.send('{}, {}'.format(city, country).title() + ' not found!')
        return
    url = 'http://openweathermap.org/img/w/'
    icon_file = url + weather_json['weather_icon_name'] + '.png'
    icon = urlopen(icon_file)
    with open('icon.png', 'wb') as f:
        shutil.copyfileobj(icon, f)

    temp = weather_json['temperature']['temp']
    output = 'Weather for {}, {}:\n'.format(city, country)
    output += 'status: ' + weather_json['detailed_status'] + '\n'
    output += 'cloud %: ' + repr(weather_json['clouds']) + '\n'
    output += ('temperature: Farenheit: %s, Celsius: %s' % (round(k2f(int(temp)), 1), round(k2c(int(temp)), 1))) + '\n'

    await ctx.send(output, file=discord.File('icon.png'))
    
    


@bot.command()
async def joke(ctx):
    """
    sends a random joke from https://michael78912.github.io/puns.html
    """
    await ctx.send(Joker().joke)


@bot.command()
async def test(ctx, *, arg):
    print(arg.encode())

def get_details(exception):
    """
    return the details of the traceback
    """

    tbstring = ''.join(traceback.format_exception(
        type(exception), exception, exception.__traceback__))
    #tbargs = ', '.join(exception.args)
    return tbstring#, tbargs
        
    

bot.run(os.environ['TOKEN'])
