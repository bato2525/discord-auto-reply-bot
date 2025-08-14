import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 許可されたチャンネルIDを取得
ALLOWED_CHANNEL_ID = int(os.getenv('ALLOWED_CHANNEL_ID', 0))

def is_allowed_channel(channel_id: int) -> bool:
    """指定されたチャンネルでのみ反応するかチェック"""
    return ALLOWED_CHANNEL_ID == 0 or channel_id == ALLOWED_CHANNEL_ID

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'スラッシュコマンドを{len(synced)}個同期しました')
    except Exception as e:
        print(f'スラッシュコマンドの同期に失敗しました: {e}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # 許可されたチャンネルでない場合は反応しない
    if not is_allowed_channel(message.channel.id):
        await bot.process_commands(message)
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

# 通常のコマンド
@bot.command(name='ping')
async def ping(ctx):
    if not is_allowed_channel(ctx.channel.id):
        await ctx.send('このチャンネルではコマンドを使用できません。', delete_after=5)
        return
    await ctx.send('Pong!')

# スラッシュコマンド
@bot.tree.command(name='ping', description='BOTの応答速度をテストします')
async def slash_ping(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message('このチャンネルではコマンドを使用できません。', ephemeral=True)
        return
    await interaction.response.send_message('Pong! 🏓')

@bot.tree.command(name='hello', description='挨拶をします')
async def slash_hello(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message('このチャンネルではコマンドを使用できません。', ephemeral=True)
        return
    await interaction.response.send_message(f'こんにちは、{interaction.user.mention}さん！👋')

@bot.tree.command(name='info', description='BOTの情報を表示します')
async def slash_info(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message('このチャンネルではコマンドを使用できません。', ephemeral=True)
        return
    embed = discord.Embed(
        title="BOT情報",
        description="Discord自動返信BOT",
        color=discord.Color.blue()
    )
    embed.add_field(name="機能", value="• 自動返信\n• スラッシュコマンド\n• メンション応答", inline=False)
    embed.add_field(name="コマンド", value="• `/ping` - 応答テスト\n• `/hello` - 挨拶\n• `/info` - この情報", inline=False)
    embed.add_field(name="制限", value=f"• チャンネルID: {ALLOWED_CHANNEL_ID}", inline=False)
    if bot.user:
        embed.set_footer(text=f"Made by {bot.user.name}")
    await interaction.response.send_message(embed=embed)

if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print('DISCORD_TOKENが設定されていません。.envファイルを確認してください。')