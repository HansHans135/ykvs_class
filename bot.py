import discord
import json
import asyncio

with open ("setting.json","r")as f:
    setting=json.load(f)
bot = discord.Bot(intents=discord.Intents.all())
cl = []

@bot.event
async def on_ready():
    print(bot.user)

@bot.event
async def on_message(msg:discord.Message):
    if msg.author.id ==985775670661632000:
        if int(msg.content) <5:
            m=await msg.reply("要講就講多一點")
        elif int(msg.content) <10:
            m=await msg.reply("喔是喔")
        else:
            m=await msg.reply("吵屁喔包蛋")
            await msg.add_reaction("🥚")
            await msg.add_reaction("⛔")
        await asyncio.sleep(10)
        await m.delete()
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and after.channel.id == 1148583730546491392:
        guild = member.guild
        name = member.name
        new_channel = await guild.create_voice_channel(name, category=after.channel.category)
        await member.move_to(new_channel)
        cl.append(new_channel.id)
    elif before.channel is not None and before.channel.id in cl and len(before.channel.members) == 0:
        await before.channel.delete()
        cl.remove(before.channel.id)

bot.run(setting["token"])
