import webbrowser
from topnews import get_today_news
from win10toast_click import ToastNotifier
import json
import time
import datetime
from datetime import datetime


def open_link(link):
    try:
        webbrowser.open(link)
    except Exception as e:
        print(f"Cannot open the link: {e}")


def get_seen_news_from_JSON():
    try:
        with open('seen_news.json', 'r', encoding='utf-8') as f:
            file_contents = f.read().strip()
            if not file_contents:
                return []
            seen_news = json.loads(file_contents)
            if not isinstance(seen_news, list):
                raise ValueError("JSON data is not a list")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading JSON file: {e}")
        seen_news = []
    return seen_news


def save_news_to_JSON(seen_news):
    with open('seen_news.json', 'w', encoding='utf-8') as f:
        json.dump(seen_news, f, indent=4, ensure_ascii=False)


def is_news_seen(news_item, seen_news):
    for seen in seen_news:
        if seen['link'] == news_item['link']:
            return True
    return False


def clean_up_old_news(seen_news):
    current_date = datetime.now().strftime("%d %b %Y")
    cleaned_news = [news for news in seen_news if news['pubDate'].startswith(current_date)]
    return cleaned_news


def show_notification():
    today_news_items = get_today_news()
    i = 0
    toast = ToastNotifier()
    seen_news = get_seen_news_from_JSON()
    cleaned_news = clean_up_old_news(seen_news)
    for current_news in today_news_items:
        i += 1
        if not is_news_seen(current_news, cleaned_news):
            toast.show_toast(current_news['pubDate'], current_news['title'], duration=20,
                             callback_on_click=lambda: open_link(current_news['link']))
            cleaned_news.append(current_news)
            save_news_to_JSON(cleaned_news)
            break


frequency_mapping = {
    "1 minute": 1,
    "2 minutes": 2,
    "5 minutes": 5,
    "10 minutes": 10,
    "15 minutes": 15,
    "30 minutes": 30,
    "1 hour": 60,
    "2 hours": 120,
    "3 hours": 180,
    "6 hours": 360,
    "12 hours": 720,
    "Never": float('inf')
}


def run_service():
    print("in run service")
    while True:
        with open('user_preferences.json', 'r') as f:
            preferences = json.load(f)

        current_time = datetime.datetime.now().time()

        start_hour = preferences['start_hour']
        start_minute = preferences['start_minute']
        end_hour = preferences['end_hour']
        end_minute = preferences['end_minute']

        start_time = datetime.time(hour=start_hour, minute=start_minute)
        end_time = datetime.time(hour=end_hour, minute=end_minute)

        frequency = preferences['frequency']
        frequency_minutes = frequency_mapping.get(frequency, float('inf'))

        if start_time <= current_time <= end_time or (
                start_time > end_time and (current_time >= start_time or current_time <= end_time)):
            show_notification()
            time.sleep(frequency_minutes * 60)


if __name__ == "__main__":
    # run_service()
    show_notification()
