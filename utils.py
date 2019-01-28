import discord
from random import choice
import time
import feedparser
import requests
from bs4 import BeautifulSoup

def mock_message(msg:str):
    """
    Spongebob mocks the given input by randomly varying the case of each letter.

    Parameters:
        msg (str): Message to mock.

    Returns:
        str: Mocked message.
    """
    returnMsg = ""

    for char in msg:
        returnMsg += choice((char.upper, char.lower))()

    return returnMsg

async def get_message(ctx, message:int):
    """
    Returns a previous message for a given channel and location (relative to context).

    Parameters:
        ctx (context): Passthrough for context from command.
        message (int): Location of message relative to sent command.

    Returns:
        Message: The message object of the selected message.
    """
    channel = ctx.message.channel
    history = await channel.history().flatten()

    returnMsg = history[message]
    return returnMsg

async def get_text(ctx, inputArg):
    """
    Returns the text given as the argument or the message from history with the author.

    Parameters:
        ctx (context): Passthrough for context from command.
        inputArg (string): Argument given from user.
    
    Returns:
        message, author (tuple): The message to be modified and author if applicable.
    """
    author = ""
    if str.isdigit(inputArg):
        inputArg = int(inputArg)
        if inputArg > 99:
            await ctx.send("Hey mate, I can only get history for the past 99 messages.")
            return
        else:
            msgRaw = await get_message(ctx, inputArg)
            author = f"**{msgRaw.author.display_name}:** "
            msg = msgRaw.content
    else:
        msg = inputArg

    return msg, author

def get_xkcd():
    """
    Returns the latest xkcd comic URL

    Returns:
        str: The URL to the latest xkcd comic
    """
    xkcd_feed =  "https://xkcd.com/rss.xml"
    d = feedparser.parse(xkcd_feed)

    latest = d["entries"][0]
    return latest["link"]

def jims_picker():
    """
    Picks a random Jim's group company

    Returns:
        str: A Jim's group company
    """
    companies = []
    with open("jims.txt", mode="r") as data:
        for company in data :
            companies.append(company)
    selection = choice(companies)
    return f"Jim's {selection}"

def today_holiday():
    html = requests.get("https://www.timeanddate.com/holidays/fun/").content
    soup = BeautifulSoup(html, 'html.parser')

    holiday = soup.find(class_="hl").a.string

    return holiday