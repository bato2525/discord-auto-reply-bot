import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 許可されたチャンネルIDを取得
ALLOWED_CHANNEL_ID = int(os.getenv('ALLOWED_CHANNEL_ID', 0))

def is_allowed_channel(channel_id: int | None) -> bool:
    """指定されたチャンネルでのみ反応するかチェック"""
    if channel_id is None:
        return False
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
    
    # コマンドの場合は処理しない（コマンド処理に任せる）
    if message.content.startswith('!') or message.content.startswith('/'):
        await bot.process_commands(message)
        return
    
    # メンションされた場合は特別な応答
    if bot.user and bot.user.mentioned_in(message):
        await message.channel.send('何かご用でしょうか？')
    else:
        # 通常のメッセージはオウム返し
        await message.channel.send(message.content)
    
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    # BOT自身のリアクションは無視
    if bot.user and payload.user_id == bot.user.id:
        return
    
    # 許可されたチャンネルでない場合は反応しない
    if not is_allowed_channel(payload.channel_id):
        return
    
    # サムズアップ（👍）のリアクションをチェック
    if str(payload.emoji) == '👍':
        channel = bot.get_channel(payload.channel_id)
        if channel and hasattr(channel, 'send'):
            await channel.send('グッドマークが押されたよ')

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

@bot.tree.command(name='echo', description='入力したテキストをオウム返しします')
async def slash_echo(interaction: discord.Interaction, text: str):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message('このチャンネルではコマンドを使用できません。', ephemeral=True)
        return
    await interaction.response.send_message(text)

@bot.tree.command(name='info', description='BOTの情報を表示します')
async def slash_info(interaction: discord.Interaction):
    if not is_allowed_channel(interaction.channel_id):
        await interaction.response.send_message('このチャンネルではコマンドを使用できません。', ephemeral=True)
        return
    embed = discord.Embed(
        title="BOT情報",
        description="Discordオウム返しBOT",
        color=discord.Color.blue()
    )
    embed.add_field(name="機能", value="• メッセージのオウム返し\n• スラッシュコマンド\n• メンション応答\n• サムズアップリアクション応答", inline=False)
    embed.add_field(name="コマンド", value="• `/ping` - 応答テスト\n• `/hello` - 挨拶\n• `/echo` - オウム返し\n• `/info` - この情報", inline=False)
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