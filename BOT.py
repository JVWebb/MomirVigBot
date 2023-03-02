import discord
from discord.ext import commands
import requests
import json
import random

intents = discord.Intents.default()

description = '''Momir Vig will give you a random creature with a given mana value.'''

bot = commands.Bot(command_prefix="", case_insensitive=True, description=description, intents=intents)

def get_card(cmc):
    if cmc < 17 and not cmc < 0:
        cmccode = ("f:vintage+type:creature+cmc=" + str(cmc))
        usingURL = "https://api.scryfall.com/cards/random?q=" + cmccode
        card = requests.get(usingURL)
        cardinfo = json.loads(card.content)
        return cardinfo["name"], cardinfo["image_uris"]["normal"]
    if cmc > 16:
        return ("No creature is powerful enough to warrant more than 16 mana!", "")
    else:
        return ("Some error occurred in my calculations!", "")

def yugioh_bs(level):
    if level > 0 and level < 13:
        usingURL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?level=" + str(level)
        card = requests.get(usingURL)
        cardinfo = json.loads(card.content)["data"]
        currentcard = cardinfo[random.randint(0,len(cardinfo))]
        return currentcard["name"], currentcard["card_images"][0]["image_url"]
    if level > 12:
        return ("No monster is stronger than a level 12!\nExcept that one card, but who cares about that.", "https://images.ygoprodeck.com/images/cards/15862758.jpg")
    else:
        return ("Some error occurred in my calculations!", "")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def momir(ctx, number: int):
    """Gives a random creature with given mana value."""
    card = get_card(number)
    embedded = discord.Embed(title=card[0])
    embedded.set_image(url=card[1])
    await ctx.send(embed=embedded)

@bot.command()
async def yugioh(ctx, number: int):
    """Gives a random monster of the given level."""
    card = yugioh_bs(number)
    embedded = discord.Embed(title=card[0])
    embedded.set_image(url=card[1])
    await ctx.send(embed=embedded)

bot.run('TOKEN')
