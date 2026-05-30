import discord
import os
from datetime import datetime
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

is_active = True

@client.event
async def on_ready():
    print(f'로그인 완료: {client.user}')

@client.event
async def on_message(message):
    global is_active 
    
    if message.author == client.user:
        return

    if message.content == '/NATO':
        await message.channel.send('online 입니다')

    if message.content == '/ON':
        is_active = True
        await message.channel.send('🔊 입장 알림 기능이 켜졌습니다.')
    elif message.content == '/OFF':
        is_active = False
        await message.channel.send('🔇 입장 알림 기능이 꺼졌습니다.')

@client.event
async def on_voice_state_update(member, before, after):
    if is_active and before.channel != after.channel and after.channel:
        now = datetime.now()
        time_str = now.strftime("%Y-%m-%d %H:%M:%S") 
        
        # 지정하신 채널 ID로 텍스트 채널을 가져옴
        log_channel = client.get_channel(1510153144108322967)
        
        # 해당 채널이 존재할 때만 메시지 전송 (음성 채널에는 보내지 않음)
        if log_channel:
            await log_channel.send(f"[{time_str}] {after.channel.name}에 {member.display_name}님이 들어왔어요!")

# 봇 실행 전에 웹 서버 켜기
keep_alive() 

# 환경 변수에서 토큰을 가져와서 실행
client.run(os.environ['BOT_TOKEN'])
