import discord
import json
import asyncio
from datetime import datetime,timezone,timedelta
from discord.ext import commands

with open ("setting.json","r")as f:
    setting=json.load(f)

cl = []
user_ls=[]

class PersistentViewBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),intents=discord.Intents.all()
        )
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(yn())
            self.persistent_views_added = True

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")
bot=PersistentViewBot()

class yn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="重新整理",
        style=discord.ButtonStyle.gray,
        custom_id="awa:yes",
    )
    async def green(self, button: discord.ui.Button, interaction: discord.Interaction):
        with open("money.json","r")as f:
            data=json.load(f)
        text=""
        num=0
        for i in data :
            if data[i]!=0:
                text+=f"<@{i}> : {data[i]}$\n"
                num+=data[i]
        embed=discord.Embed(title=f"所有欠錢的人",description=text)
        embed.set_footer(text=f"所以總共有 {num}$ 要收款")
        await interaction.response.edit_message(embed=embed)


@bot.event
async def on_message(msg:discord.Message):
    if msg.author.id ==985775670661632000:
        if len(msg.content) <5:
            await msg.reply("要講就講多一點")
        elif len(msg.content) <10:
            await msg.reply("喔是喔")
        else:
            await msg.reply("吵屁喔包蛋")
            await msg.add_reaction("🥚")
            await msg.add_reaction("⛔")

@discord.message_command(name="刪除訊息")
async def dle(ctx: discord.ApplicationContext, message: discord.Message):
    if message.author.name==bot.user.name:
        if message.content in ["要講就講多一點","喔是喔","吵屁喔包蛋"]:
            await message.delete()
            await ctx.respond("done",ephemeral=True)

@bot.slash_command(description="修改錢錢")
async def edit(ctx:discord.ApplicationContext,user:discord.Member,title:str,money:int):
    if ctx.user.id !=851062442330816522:
        await ctx.respond("還想偷改阿細狗")
        return
    
    with open("money.json","r")as f:
        data=json.load(f)
    try:
        data[str(user.id)]+=money
    except:
        data[str(user.id)]=money
    with open("money.json","w+")as f:
        json.dump(data,f)

    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    now = dt2.strftime("%Y-%m-%d")
    with open(f"money/{user.id}","a+")as f:
        f.write(f"{now} | {title} {money}$\n")
    await ctx.respond(f"{now} | {title} {money}$",ephemeral=True)

@bot.slash_command(description="查看錢錢紀錄")
async def money(ctx:discord.ApplicationContext,user:discord.Member):
    with open(f"money/{user.id}","r")as f:
        text=f.read()
    with open("money.json","r")as f:
        data=json.load(f)
    embed=discord.Embed(title=f"{user.name}的紀錄",description=text)
    embed.set_footer(text=f"所以他還欠 {data[str(user.id)]}$")
    await ctx.respond(embed=embed)

@bot.slash_command(description="查看錢錢列表")
async def list(ctx:discord.ApplicationContext):
    with open("money.json","r")as f:
        data=json.load(f)
    text=""
    num=0
    for i in data :
        if data[i]!=0:
            text+=f"<@{i}> : {data[i]}$\n"
            num+=data[i]
    embed=discord.Embed(title=f"所有欠錢的人",description=text)
    embed.set_footer(text=f"所以總共有 {num}$ 要收款")
    await ctx.respond(embed=embed, view=yn())

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

    vc_cls=bot.get_channel(1165519977437208616)
    if after.channel:
        if before.channel!=after.channel and member.id not in user_ls:
            user_ls.append(member.id)
            embed=discord.Embed(title="加入語音",description=f"<@{member.id}> 加入了 <#{after.channel.id}>",color=discord.Color.green())
            await vc_cls.send(embed=embed)
    elif before.channel:
        user_ls.remove(member.id)
        embed=discord.Embed(title="退出語音",description=f"<@{member.id}> 退出了 <#{before.channel.id}>",color=discord.Color.red())
        await vc_cls.send(embed=embed)

bot.run(setting["token"])
