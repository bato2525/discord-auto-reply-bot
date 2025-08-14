import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    content = message.content.lower()
    
    if 'こんにちは' in content or 'hello' in content:
        await message.channel.send(f'こんにちは、{message.author.mention}さん！')
    elif 'おはよう' in content or 'good morning' in content:
        await message.channel.send(f'おはようございます、{message.author.mention}さん！')
    elif 'おやすみ' in content or 'good night' in content:
        await message.channel.send(f'おやすみなさい、{message.author.mention}さん！')
    elif 'ありがとう' in content or 'thank you' in content or 'thanks' in content:
        await message.channel.send(f'どういたしまして、{message.author.mention}さん！')
    elif bot.user and bot.user.mentioned_in(message):
        await message.channel.send(f'{message.author.mention}さん、何かご用でしょうか？')
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong!')

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print('DISCORD_TOKENが設定されていません。.envファイルを確認してください。')