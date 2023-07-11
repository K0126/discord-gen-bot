import asyncio
import datetime
from lib2to3.pytree import convert
import time
from timeit import repeat
import disnake,json,os,random
from disnake.ext import commands

print(credits)
print("봇을 시작하는 중입니다...")

time.sleep(1) #간지용 쿨타임

with open("config.json") as file:
    config = json.load(file)
    token = config["token"]
    cooldown = config["cooldown"]
    cmd_channel = config["cmd_channel"]

print("-> 로딩중")

prefix = "/"
clientIntents = disnake.Intents.default()
clientIntents.message_content = True
clientIntents.members = True
venady = commands.Bot(command_prefix=prefix , intents=clientIntents, help_command=None)

time.sleep(1) #간지용 쿨타임

print("-> 로딩중")
time.sleep(1) 
print("-> 봇이 온라인입니다. \n") 

#----------------------------------------봇 이벤트----------------------------------------

@venady.event
async def on_ready():
    await venady.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.playing,
            name=f'with TellMe'),
            status=disnake.Status.online)

#----------------------------------------젠 명령어----------------------------------------

@venady.slash_command(name="젠")
@commands.cooldown(1, cooldown, commands.BucketType.member)
async def gen(inter):
    user = inter.author
    server_name = inter.guild.name
    if inter.channel.id != cmd_channel:
        await inter.send(f"<#{cmd_channel}>에서 사용하세요.")
        print(f"{inter.author.name} used 젠 -> Error [Wrong Channel]".replace(".txt",""))
        return
    stock_files = [file for file in os.listdir("Accounts") if file.endswith(".txt")]
    if len(stock_files) == 0:
        await inter.send(f"재고가 없습니다. `{prefix}재고`")
        print(f"{inter.author.name} used 젠 -> Error [No Exist Account Type]".replace(".txt",""))
        return
    stock_file = random.choice(stock_files)
    with open(f"Accounts//{stock_file}") as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            await inter.send("재고가 없습니다.")
            print(f"{inter.author.name} used 젠 -> Error [No Account Type Stock]".replace(".txt",""))
            return
    account = random.choice(lines)
    em = disnake.Embed(title=" ", description=f" \n `{str(account)}`\n  ", color=0xFFFFFF, timestamp=datetime.datetime.utcnow()) #시간 바꾸셈 ㅇㅇ
    em.set_footer(text=f"{server_name}")
    await user.send(embed=em)
    print(f"{inter.author.name} used 젠 -> Successful | {server_name}".replace(".txt",""))
    await inter.send("젠 성공! 디엠을 확인해 주세요.")

@gen.error
async def gen_error(inter: disnake.ApplicationCommandInteraction, error: Exception) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        retry_after = disnake.utils.format_dt(
            disnake.utils.utcnow() + datetime.timedelta(seconds=error.retry_after), "R"
        )
        return await inter.response.send_message(
            f"쿨타임입니다. {retry_after} 후에 다시 시도하세요. ",
            ephemeral=True
        )
    raise error

@venady.slash_command() # 재고 커멘드
async def 재고(inter:disnake.ApplicationCommandInteraction):
    """재고 확인"""
    id = inter.guild.id
    server_name = inter.guild.name
    stockmenu = disnake.Embed(title="재고", description="**종류  -  갯수** \n", color=0xFFFFFF, timestamp=datetime.datetime.utcnow())
    stockmenu.set_footer(text=f"{server_name}")
    stockmenu
    for filename in os.listdir(f"Accounts/"):
        with open(f"Accounts//{filename}") as f: 
            ammount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","") 
            stockmenu.description += f"*{name}* - {ammount}\n"
    await inter.send(embed=stockmenu)

#----------------------------------------명령어----------------------------------------

@venady.slash_command()
@commands.has_permissions(administrator=True)
async def 재고_추가(inter:disnake.ApplicationCommandInteraction, stock: disnake.Attachment):
    """재고 추가하기"""
    if not "text/plain" in stock.content_type:
        await inter.send("텍스트 파일을 넣어주세요!", ephemeral=True)
        return
    stock_bytes = await stock.read()
    stock_lines = stock_bytes.decode(stock.content_type.partition("charset=")[2]).splitlines()
    if len(stock_lines) > 5000:
        await inter.send("줄이 너무 많습니다!", ephemeral=True)
        return
    await stock.save(f"Accounts/{stock.filename}")
    await inter.send(f"{stock.filename.partition('.')[0]}이(가) 재고에 추가되었습니다.")
    return

@venady.slash_command()
@commands.has_permissions(administrator=True)
async def 재고_삭제(inter: disnake.ApplicationCommandInteraction, stock):
    """재고 삭제하기"""
    stock = stock.lower() + ".txt" 
    path = f"Accounts"
    files = os.listdir(path)
    if not stock in files:
        await inter.send("재고가 존재하지 않습니다!", ephemeral=True)
        return
    os.remove(os.path.join(path, stock))
    name = stock.lower().replace(".txt","")
    await inter.send(f"{name}이(가) 삭제되었습니다.")

venady.run(token)



# Made by TellMe#0001 (caniloveyou)
