import pprint
import time as _time
import traceback
import os
import shutil
import string
import random
os.chdir(os.path.dirname(__file__))

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen
import wikipedia

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
async def python_exec(ctx, *args: str):
    """
    executes python code, and outputs as a message.
    """
    print(args)

    code = ' '.join(args)
    if code.startswith('`'):
        code = code.strip('`')
        code = args.join('\n')
        print(code)
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

    return_str = '```python\n' + return_str + '```' if return_str != '' else 'No output'


    await ctx.send(return_str)

@python_exec.error
async def pyexc_error(ctx, error):
    pass

@bot.command()
async def joke(ctx):
    """
    sends a random joke from https://michael78912.github.io/puns.html
    """
    await ctx.send(Joker().joke)

@bot.command()
async def test(ctx):
    channel = ctx.channel
    with open('test.png', 'rb') as f:
        await channel.send(file=discord.File('test.png'))

def get_details(exception):
    """
    return the details of the traceback
    """

    tbstring = ''.join(traceback.format_exception(
        type(exception), exception, exception.__traceback__))
    #tbargs = ', '.join(exception.args)
    return tbstring#, tbargs
        
    

bot.run('NDUwNDA1Nzk4MjYzMzkwMjE5.DeyxOQ.scbD-cTS4CvePBE4dWh6DGIFEJ8')
