import schedule
import time
import random
import json
from newspaper import Article
import twitter  
import gemini
import news_driver

def load_schedule(filename="schedule.json"):
    with open(filename, 'r', encoding='utf-8') as file:
        schedule_data = json.load(file)
    return schedule_data['times']

def read_prompt_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        prompt = file.read().strip()
    return prompt

def get_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        title = article.title
        summary = article.text[:300]
        return title, summary
    except Exception as e:
        print(f"Error occurred while processing the article: {e}")
        return None, None

previous_choice = None

def post_news_to_x():
    global previous_choice

    prompt = read_prompt_from_file("prompt.txt")

    driver_functions = [
        news_driver.itemedia,
        news_driver.gizmodo,
        news_driver.gigazine,
        news_driver.mynaviz
    ]

    available_choices = [func for func in driver_functions if func != previous_choice]

    if not available_choices:
        available_choices = driver_functions

    current_choice = random.choice(available_choices)

    previous_choice = current_choice

    url = current_choice()

    title, summary = get_article(url)

    if title and summary:
        response = gemini.gemini(f'{prompt}\nTitle: {title}\nSummary: {summary}\nURL: {url}')
        send_text = f"★TechNews★\n{response}\nURL: {url}"
        print(send_text)

        # twitter.create_tweet(send_text)  # Xに投稿
    else:
        print("記事の取得に失敗しました。")

def schedule_posts():
    times = load_schedule()
    
    for post_time in times:
        schedule.every().day.at(post_time).do(post_news_to_x)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_posts()
