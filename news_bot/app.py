import json
from newspaper import Article
import google.generativeai as genai
import discord
from discord.ext import commands, tasks
import config
import asyncio
import random
from datetime import datetime, timedelta

# 各ニュースサイトのドライバー
import news_driver

# 投稿処理が進行中かどうかを示すフラグ
is_task_running = False

def get_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        summary = article.summary
        return title, summary
    except Exception as e:
        print(f"Error occurred while processing the article: {e}")
        return None, None

def read_prompt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    return prompt

def generate_text(text, driver_function):
    latest_url = driver_function()
    title, summary = get_article(latest_url)
    print(f"URL: {latest_url}\n")
    print(f"Title: {title}\n")
    print(f"Summary: {summary}")

    response = model.generate_content(
        [text + "\n" + title + "\n" + summary + "\n" + latest_url],
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    )

    generated_text = response.text
    print("Response:")
    print(generated_text)
    return generated_text

def read_send_times(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [datetime.strptime(time, "%H:%M").time() for time in data["send_times"]]

# GEMINIの設定
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# DISCORDの設定
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# ファイルからプロンプトを読み込む
prompt_file = 'prompt.txt'
prompt = read_prompt(prompt_file)

# ニュースサイトのドライバー関数リストと使用された関数のセット
driver_functions = [
    news_driver.yahoo,
    news_driver.techable,
    news_driver.itemedia,
    news_driver.gizmodo,
    news_driver.gigazine,
    news_driver.axismag,
    news_driver.mynaviz,
    news_driver.wired,
    news_driver.thebridge,
    news_driver.cne
]
used_functions = set()

async def send_scheduled_message(channel, send_times):
    global used_functions, is_task_running

    while True:
        now = datetime.now()
        next_time = None
        for send_time in send_times:
            future_time = now.replace(hour=send_time.hour, minute=send_time.minute, second=0, microsecond=0)
            if now < future_time:
                next_time = future_time
                break
        if not next_time:
            next_time = now.replace(hour=send_times[0].hour, minute=send_times[0].minute, second=0, microsecond=0) + timedelta(days=1)
        
        await discord.utils.sleep_until(next_time)
        
        if is_task_running:  # 投稿処理が進行中の場合はスキップ
            continue

        # タスク開始フラグをセット
        is_task_running = True

        try:
            # 使用されていない関数をランダムに選択
            available_functions = list(set(driver_functions) - used_functions)
            if not available_functions:
                used_functions.clear()
                available_functions = driver_functions
            
            selected_function = random.choice(available_functions)
            used_functions.add(selected_function)

            message = f"{next_time.strftime('%Y-%m-%d %H:%M:%S')}."
            await channel.send(message)
            await channel.send(generate_text(prompt, selected_function))
        finally:
            # タスク終了フラグをリセット
            is_task_running = False

@bot.event
async def on_ready():
    print("Discord-Bot ready!")
    channel = bot.get_channel(config.ALLOWED_CHANNEL_ID)
    send_times = read_send_times('send_times.json')  # 外部ファイルから送信時間を読み込む
    asyncio.create_task(send_scheduled_message(channel, send_times))

@bot.command()
async def post_news(ctx):
    global used_functions, is_task_running
    
    if is_task_running:  # 投稿処理が進行中の場合はスキップ
        await ctx.send("現在、別のタスクが進行中です。しばらくお待ちください。")
        return
    
    # タスク開始フラグをセット
    is_task_running = True

    try:
        # 使用されていない関数をランダムに選択
        available_functions = list(set(driver_functions) - used_functions)
        if not available_functions:
            used_functions.clear()
            available_functions = driver_functions
        
        selected_function = random.choice(available_functions)
        used_functions.add(selected_function)

        await ctx.send(generate_text(prompt, selected_function))
    finally:
        # タスク終了フラグをリセット
        is_task_running = False

@bot.command()
async def post_time(ctx):
    now = datetime.now()
    message = f"{now}"
    await ctx.send(message)

bot.run(config.DISCORD_TOKEN)
