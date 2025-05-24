import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime

# ブログのURL
BASE_URL = 'https://www.kokuei-film.com/blog/maiika/'

# HTMLを取得
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# RSSフィードの基本情報を設定
fg = FeedGenerator()
fg.title('まいーかブログ')
fg.link(href=BASE_URL, rel='alternate')
fg.description('国映株式会社「まいーか」の公式ブログRSSフィード')
fg.language('ja')

# 記事ブロックを探してパース
for article in soup.select('.blog-post-list li'):
    title_tag = article.find('a')
    if not title_tag:
        continue

    title = title_tag.text.strip()
    link = title_tag['href']
    full_link = link if link.startswith('http') else BASE_URL + link.lstrip('/')

    date_tag = article.find('span', class_='blog-post-date')
    pubDate = None
    if date_tag:
        try:
            pubDate = datetime.strptime(date_tag.text.strip(), '%Y.%m.%d')
        except ValueError:
            pass

    fe = fg.add_entry()
    fe.title(title)
    fe.link(href=full_link)
    if pubDate:
        fe.pubDate(pubDate)

# RSSフィードを書き出し
fg.rss_file('../maiika_feed.xml', encoding='utf-8')


