import os
from dotenv import load_dotenv
import discord
from discord import option

from scraper import Scraper
from downloader import Downloader

# On charge le fichier .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # Récupère DISCORD_TOKEN

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

@bot.slash_command(name="var", description="Scrape et télécharge les vidéos d'un site LeFive, puis les envoie ici.")
@option("url", str, description="Lien du site LeFive", required=True)
async def var_command(ctx: discord.ApplicationContext, url: str):
    await ctx.respond(f"Scraping .. euuh Vérification de la var en cours pour: {url} ...", ephemeral=True)

    scraper = Scraper()
    scraper.scrap_five_website(url)

    downloader = Downloader(src="playlist.txt", path="./downloads")
    downloader.download_dailymotion_videos_from_playlist()

    import os
    sent_count = 0
    for filename in os.listdir("./downloads"):
        if filename.lower().endswith((".mp4", ".mkv", ".mov", ".avi")):
            file_path = os.path.join("./downloads", filename)
            await ctx.channel.send(file=discord.File(file_path))
            sent_count += 1

    await ctx.respond(f"{sent_count} vidéos envoyées dans ce channel.", ephemeral=True)

if __name__ == "__main__":
    bot.run(TOKEN)
