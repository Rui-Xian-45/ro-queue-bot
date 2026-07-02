import discord
from discord.ext import commands
import os

from views import QueueView
from embeds import build_embed
from queue_manager import QueueManager

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

queue = QueueManager()


@bot.event
async def on_ready():
    print(f"✅ {bot.user}")

    bot.add_view(QueueView())


@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):

    if queue.data["message_id"]:
        return await ctx.send("⚠ 已建立")

    msg = await ctx.send(embed=build_embed(), view=QueueView())

    queue.data["message_id"] = msg.id
    queue.data["channel_id"] = ctx.channel.id
    queue.save()

    await ctx.send("✅ 完成")


async def update_panel():

    if not queue.data["message_id"]:
        return

    channel = bot.get_channel(queue.data["channel_id"])
    msg = await channel.fetch_message(queue.data["message_id"])

    await msg.edit(embed=build_embed(), view=QueueView())


@bot.command()
async def refresh(ctx):
    await update_panel()
    await ctx.send("🔄 OK")


TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
