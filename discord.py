import nextcord, asyncio
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
from nextcord import application_command
import time
from timeit import repeat


print(credits)
print("봇을 시작하는 중입니다...")

print("-> 로딩중")

time.sleep(1) #간지용 쿨타임

time.sleep(1) #간지용 쿨타임

print("-> 로딩중")
time.sleep(1) 
print("-> 봇이 온라인입니다. \n")


intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

admins = [1234, 5678] # 관리자 아이디 추가


def getAcc():
    with open('acc.txt', 'r') as f:
        accounts = f.readlines()
        f.close()
    if len(accounts) == 0:
        return False
    account = accounts[0].replace("\n", "")
    accounts = [acc.strip() for acc in accounts if acc.strip() != account]
    with open('acc.txt', 'w') as file:
        file.write('\n'.join(accounts))
    return account


def checkCount():
    with open('acc.txt', 'r') as f:
        accounts = f.readlines()
        f.close()
    return len(accounts)


@bot.slash_command(name="젠", description="DM으로 재고 전송")
async def 젠(interaction: Interaction):
    if interaction.channel.id != 1128409819448082445: # 커멘드 사용 가능한 채널 아이디 
        return await interaction.send('**```css\n[ ⛔ ] 해당 채널에서는 명령어를 사용할 수 없어요!```**')
    acc = getAcc()
    if acc == False:
        return await interaction.send('**```css\n[ ⛔ ] 재고가 없습니다!```**')
    try:
        em = nextcord.Embed(title=" ", description=f" \n `{acc}`\n  ", color=0x5d6bde )
        await interaction.user.send(embed=em)
        await interaction.send('**```css\n[ ✅ ] DM을 확인해주세요!```**')
    except:
        return await interaction.send('**```css\n[ ⛔ ] DM 전송에 실패하였습니다.```**')


@bot.slash_command(name="재고확인", description="남은 재고 확인")
async def 재고확인(interaction: Interaction):
    if interaction.user.id in admins or interaction.channel.id == 1128409819448082445: # 커맨드 사용 가능한 채널 아이디 
        count = checkCount()
        await interaction.send(f'**```css\n 남은 재고는 {count}개 입니다.```**')
    else:
        await interaction.send('**```css\n해당 채널에서는 명령어를 사용할 수 없어요!```**')



bot.run('token') #token에 봇 토큰 추가
