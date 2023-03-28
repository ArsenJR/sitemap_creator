import threading
import time

from requests_html import HTMLSession

from urllib.parse import urljoin, urlparse

from update_data import add_sitemap_creations, add_sitemaps_links_requests_html

HOMEPAGE_URL = 'http://www.stackoverflow.com/'
HOMEPAGE_URL_v2 = 'https://stackoverflow.com/'
#HOMEPAGE_URL = 'http://www.crawler-test.com/'
DOMEN_NAME_1 = urlparse(HOMEPAGE_URL).netloc
DOMEN_NAME_2 = urlparse(HOMEPAGE_URL_v2).netloc
DOMEN_ZONE = DOMEN_NAME_1.split('.')[2]

DEFAULT_COUNT_THREADS = len(threading.enumerate())

all_urls = set()
all_urls.clear()
#all_urls.add(HOMEPAGE_URL)
urls_relation = {}

global depth
depth = 0

def get_urls_on_page(url: str):
    """
        :param url: url адрес
        :return: возвращает список ссылок, найденных на странице
    """
    global all_urls

    all_urls.add(url)

    if url.endswith('/'):
        url = url[:-1]

    session = HTMLSession()
    try:
        request = session.get(url)
        links_on_page = request.html.links
    except:
        return

    urls_with_same_domain = set()
    urls_with_another_domain = set()

    for link in links_on_page:
        link = urljoin(HOMEPAGE_URL, link)
        # проверяем доменное имя

        netloc = urlparse(link).netloc
        if netloc == DOMEN_NAME_2 or netloc == DOMEN_NAME_1:
            urls_with_same_domain.add(link)
        else:
            urls_with_another_domain.add(link)

        # заполняем новые ссылки в карту сайта
    urls_relation[url] = urls_with_same_domain.union(urls_with_another_domain)
    for founded_url in urls_with_another_domain:
        # созраняю url с другим доменом
        all_urls.add(founded_url)

    return urls_with_same_domain

def do_sitemap(url: str):
    """
        Сканирует веб-страницу и извлекает все ссылки.
        Ссылки можно найти в переменной 'all_urls'
    """
    global depth
    global all_urls

    urls_with_same_domain = get_urls_on_page(url)

    if not urls_with_same_domain:
        # подходящих url не найдено на странице
        return

    for founded_url in urls_with_same_domain:
        if founded_url in all_urls:
            # url уже рассматривался
            continue

        if depth > 1000:
            # привешение лимита
            return

        depth += 1
        thread = threading.Thread(target=do_sitemap, args=(founded_url, ))
        thread.start()

    return
if __name__ == "__main__":

    start = time.time()
    do_sitemap(HOMEPAGE_URL)

    print('Слежу за потоками:')
    while (DEFAULT_COUNT_THREADS != len(threading.enumerate())):
        print('Всего активных потоков:', len(threading.enumerate()))
        time.sleep(5)

    print('Потоков стандартное количество')
    end = time.time() - start

    print()
    print('Отчет')
    print(f'URL: {HOMEPAGE_URL}')
    print(f'Время обработки: {int(end)} сек')
    print(f'Количество найденных ссылок: {len(all_urls)} ')

    f = open(r'requests_html_results/stackoverflow.txt', 'w', encoding="utf-8")
    f.write(f'ОТЧЕТ \n \n')
    f.write(f'URL: {HOMEPAGE_URL} \n')
    f.write(f'Время обработки: {int(end)} \n')
    f.write(f'Количество найденных ссылок: {len(all_urls)} \n \n \n ')
    f.write(f'Список ссылок: \n {all_urls} \n \n \n ')
    f.write(f'Зависимости: \n {urls_relation} \n \n \n ')
    f.close()

    results = (HOMEPAGE_URL, 'requests_html', len(all_urls), int(end))
    add_sitemap_creations(results)

    site_nodes = []
    for parent_url in urls_relation:
        for url in urls_relation[parent_url]:
            site_nodes.append((HOMEPAGE_URL, parent_url, url))
    add_sitemaps_links_requests_html(site_nodes)
