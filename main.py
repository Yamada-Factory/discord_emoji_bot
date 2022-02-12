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

@bot.slash_command(guild_ids=SCOPE)
async def emojigen(
    ctx: discord.ApplicationContext,
    text: Option(str, "content text"),
    color: Option(str, "font color (default: #000000FF)", default="#000000FF"),
    background_color: Option(str, "back ground color (default: #00000000)", default="#00000000"),
    align: Option(str, "choose text align (default: center)", choices=["left", "center", "right"], default="center"),
    font: Option(str, "choose font (default: NotoSansJP-Regular", choices=font_map.keys(), default="NotoSansJP-Regular")
    ):
    
    text = text.replace('\\n', '\n')
    data = emojilib.generate(
        text=text,
        color=color,
        background_color=background_color,
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
    color: Option(str, "font color (default: #000000FF)", default="#000000FF"),
    background_color: Option(str, "back ground color (default: #00000000)", default="#00000000"),
    align: Option(str, "choose text align (default: center)", choices=["left", "center", "right"], default="center"),
    font: Option(str, "choose font (default: NotoSansJP-Regular", choices=font_map.keys(), default="NotoSansJP-Regular")
    ):
    
    text = text.replace('\\n', '\n')
    data = emojilib.generate(
        text=text,
        color=color,
        background_color=background_color,
        align=align,
        typeface_file=font_map[font],
        width=128,
        height=128
    )
    emoji = await ctx.interaction.guild.create_custom_emoji(name=name, image=data)

    await ctx.respond(emoji)

print('server started')
bot.run(TOKEN)
