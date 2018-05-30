import pprint
import time as _time
import traceback

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen

from stdabsorb import StdAbsorber
bot = commands.Bot(command_prefix=">", description='A bot that greets the user back.')
client = discord.Client()


@bot.command()
async def snowman(ctx):
    await ctx.send("lol you expected, a snowman, but i can't do that, so have an 8.")


@bot.command()
async def mention(ctx):
    await ctx.send(ctx.author.mention)

@bot.command()
async def time_in_kelowna(ctx):
    await ctx.send(_time.asctime())

@bot.command()
async def see_kelowna(ctx):
    # server = client.get_server()
    soup = BeautifulSoup(urlopen('https://www.castanet.net/scenic-web-cams/camera/7/', ))
    division = soup.find('img', {'id': 'camImage', 'alt': 'Downtown Kelowna'})
    img = division.get_attribute_list('src')[0]
    await ctx.send('image of kelowna: ' + img)

@bot.command()
async def python_exec(ctx, code):
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

    return_str = '```python\n' + return_str + '```'


    await ctx.send(return_str)
    

@bot.command()
async def get_help(ctx):
    help_str = """```RandomBot- a completely random and useless bot
It is still being developed, so it can become even more useless in
the long run.

commands:

    snowman: display a snowman
    mention: mention the sender
    time_in_kelowna: send the current time in Kelowna, BC, Canada.
    see_kelowna: send a picture of the current webcam shot of kelowna, as viewed from Knox mountain.
    python_exec: executes python code, and outputs as a message.

    more coming soon! this bot will only work when I'm online, so have fun.```
"""
    await ctx.send(help_str)

def get_details(exception):
    """
    return the details of the traceback
    """

    tbstring = ''.join(traceback.format_exception(
        type(exception), exception, exception.__traceback__))
    #tbargs = ', '.join(exception.args)
    return tbstring#, tbargs
        
    

bot.run('NDUwNDA1Nzk4MjYzMzkwMjE5.DeyxOQ.scbD-cTS4CvePBE4dWh6DGIFEJ8')
