import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import Context

from Pythactyl.Client import PterodactylClient

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

url = "https://pterodactyl.panel"


if "accounts.json" not in os.listdir():
    with open("../../accounts.json", "w") as fw:
        json.dump({"users": []}, fw)

async def testPanelConnection(token):
    client = PterodactylClient("https://panel.jgamingz.dev", token)
    if client.account().id is not None:
        return True
    else:
        return False

async def checkUserExists(id: int):
    with open("../../accounts.json", "r") as fr:
        users = json.load(fr)
    for user in users['users']:
        if user['id'] == id:
            return True
    return False


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def connect(ctx: Context):
    if await checkUserExists(ctx.author.id): # If the user already exists in the Database then skip them to save duplicate data
        await ctx.send(f'{ctx.author.display_name} You are already connected to Pterodactyl!')
        return

    await ctx.send(f'{ctx.author.display_name} I have dm\'d you!')
    await ctx.author.send("Paste your user API Token here (DO NOT SHARE THIS WITH ANYONE)!")
    token = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=360.0)
    token = token.content
    if token is not None:
        if await testPanelConnection(token):
            with open("../../accounts.json", "r") as fr:
                users = json.load(fr)

            user = {
                "id": ctx.author.id,
                "name": ctx.author.display_name,
                "token": token
            }
            users['users'].append(user)

            with open("../../accounts.json", "w") as f:
                json.dump(users, f, indent=2)
            await ctx.send(f'{ctx.author.display_name} Connected to Pterodactyl!')

@bot.command()
async def servers(ctx: Context):

    if not await checkUserExists(ctx.author.id):
        await ctx.send(f'{ctx.author.display_name} You are not connected to Pterodactyl!')
        return
    with open("../../accounts.json", "r") as fr:
        users = json.load(fr)

    for user in users['users']:
        if user['id'] == ctx.author.id:
            token = user['token']
    client = PterodactylClient(url, token)

    servers = client.listServers()
    embed = discord.Embed(title="Servers", color=0x00ff00)
    _a = ""
    for server in servers:
        _a += server.__str__() + "\n"
    embed.description = _a
    await ctx.send(embed=embed)


@bot.command()
async def stopserver(ctx: Context, serverId):
    if not await checkUserExists(ctx.author.id):
        await ctx.send(f'{ctx.author.display_name} You are not connected to Pterodactyl!')
        return
    with open("../../accounts.json", "r") as fr:
        users = json.load(fr)

    for user in users['users']:
        if user['id'] == ctx.author.id:
            token = user['token']
    client = PterodactylClient(url, token)

    servers = client.listServers()
    for server in servers:
        if server.identifier == serverId:
            client.sendPowerAction(server.identifier, "stop")
            await ctx.send("Server stopped!")

@bot.command()
async def startserver(ctx: Context, serverId):
    if not await checkUserExists(ctx.author.id):
        await ctx.send(f'{ctx.author.display_name} You are not connected to Pterodactyl!')
        return
    with open("../../accounts.json", "r") as fr:
        users = json.load(fr)

    for user in users['users']:
        if user['id'] == ctx.author.id:
            token = user['token']
    client = PterodactylClient(url, token)

    servers = client.listServers()
    for server in servers:
        if server.identifier == serverId:
            client.sendPowerAction(server.identifier, "start")
            await ctx.send("Server started!")

bot.run("")