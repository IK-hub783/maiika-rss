import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = 'https://www.kokuei-film.com/blog/maiika/'

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

fg = FeedGenerator()
fg.title('まーイーカ2 ブログ')
fg.link(href=BASE_URL, rel='alternate')
fg.description('国映株式会社「まーイーカ2」ブログの非公式RSSフィード')
fg.language('ja')

articles = soup.select('.c-blog-list__item')

for article in articles:
    a_tag = article.find('a')
    if not a_tag:
        continue

    title = a_tag.get_text(strip=True)
    href = a_tag['href']
    full_link = urljoin(BASE_URL, href)

    date_tag = article.select_one('.c-blog-list__date')
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

fg.rss_file('maiika_feed.xml', encoding='utf-8')

