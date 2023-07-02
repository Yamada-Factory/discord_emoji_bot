import emojilib
import discord
from discord.commands import Option

import tempfile
import os
import glob

TOKEN = os.getenv('TOKEN')
SCOPE = os.getenv('SERVER_IDS').split(',')

bot = discord.Bot()

def get_font_map():
    file_list = glob.glob('fonts/*')
    font_map = dict()
    for file_path in file_list:
        f = file_path.replace('fonts/', '').replace('.otf', '').replace('.ttf', '')
        font_map[f] = file_path
    return font_map

font_map = get_font_map()

def format_color(color):
    hasSharp = (color[0] == '#')
    length = len(color)
    if hasSharp:
        length -= 1
    if length == 6:
        color += 'FF'
    if not hasSharp:
        color = '#' + color
    return color


@bot.slash_command(guild_ids=SCOPE)
async def emojigen(
    ctx: discord.ApplicationContext,
    text: Option(str, "content text"),
    color: Option(str, "font color (default: #000000)", default="#000000"),
    align: Option(str, "choose text align (default: center)", choices=["left", "center", "right"], default="center"),
    font: Option(str, "choose font (default: NotoSansJP-Regular", choices=font_map.keys(), default="NotoSansJP-Regular")
    ):

    text = text.replace('\\n', '\n')
    color = format_color(color)
    data = emojilib.generate(
        text=text,
        color=color,
        align=align,
        typeface_file=font_map[font],
        width=128,
        height=128
    )
    fp = tempfile.TemporaryFile()
    fp.write(data)
    fp.seek(0)

    await ctx.respond(file=discord.File(fp, filename="emoji.png"))


@bot.slash_command(guild_ids=SCOPE)
async def emojireg(
    ctx: discord.ApplicationContext,
    name: Option(str, "emoji name"),
    text: Option(str, "content text"),
    color: Option(str, "font color (default: #000000)", default="#000000"),
    align: Option(str, "choose text align (default: center)", choices=["left", "center", "right"], default="center"),
    font: Option(str, "choose font (default: NotoSansJP-Regular", choices=font_map.keys(), default="NotoSansJP-Regular")
    ):
    
    text = text.replace('\\n', '\n')
    color = format_color(color)
    data = emojilib.generate(
        text=text,
        color=color,
        align=align,
        typeface_file=font_map[font],
        width=128,
        height=128
    )
    emoji = await ctx.interaction.guild.create_custom_emoji(name=name, image=data)

    await ctx.respond(emoji)

# refer to https://github.com/Pycord-Development/pycord/blob/20598d4a737e9f61631701e5e84fd2d4fd2cdacd/examples/create_private_emoji.py
@bot.slash_command(guild_ids=SCOPE)
async def add_emoji(
    ctx: discord.ApplicationContext,
    name: Option(str, "emoji name"),
    image: Option(discord.Attachment, "image file"),
    ):
    allowed_content_types = [
        "image/jpeg",
        "image/png",
    ]
    if image.content_type not in allowed_content_types:
        return await ctx.respond("Invalid attachment type.", ephemeral=True)

    image_file = await image.read()

    emoji = await ctx.interaction.guild.create_custom_emoji(name=name, image=image_file)
    await ctx.respond(emoji)

print('server started')
bot.run(TOKEN)
