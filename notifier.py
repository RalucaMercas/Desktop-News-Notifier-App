import time
import webbrowser
from topnews import top_stories
from win10toast_click import ToastNotifier
import json


def open_link():
    try:
        webbrowser.open(link)
    except Exception as e:
        print(f"Cannot open the link: {e}")


def load_seen_news_from_JSON():
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


news_items = top_stories()
i = 0
toast = ToastNotifier()
seen_news = load_seen_news_from_JSON()
for current_news in news_items:
    link = current_news['link']
    i += 1
    if not is_news_seen(current_news, seen_news):
        toast.show_toast(current_news['pubDate'], current_news['title'], duration=20, callback_on_click=open_link)
        seen_news.append(current_news)
        save_news_to_JSON(seen_news)
        time.sleep(15)
