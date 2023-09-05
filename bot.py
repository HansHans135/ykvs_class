import discord
import json

with open ("setting.json","r")as f:
    setting=json.load(f)
bot = discord.Bot()
cl = []

@bot.event
async def on_ready():
    print(bot.user)

@bot.event
async def on_voice_state_update(member, before, after):

    if before.channel is None and after.channel is not None and after.channel.id == 1148583730546491392:
        guild = member.guild
        name = f"{member.name}"
        new_channel = await guild.create_voice_channel(name, category=after.channel.category)
        await member.move_to(new_channel)
        cl.append(new_channel.id)
    elif before.channel is not None and before.channel.id in cl and len(before.channel.members) == 0:
        await before.channel.delete()
        cl.remove(before.channel.id)

bot.run(setting["token"])
