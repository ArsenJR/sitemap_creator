import threading
import time

from html.parser import HTMLParser

from urllib.parse import urlparse, urljoin
from urllib.request import urlopen

from update_data import add_sitemap_creations, add_sitemaps_links_urllib



HOMEPAGE_URL = 'https://www.vk.com/'
HOMEPAGE_URL_v2 = 'https://vk.com/'
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


class LinkParser(HTMLParser):
    __link_list = []

    def __init__(self):
        super(LinkParser, self).__init__(convert_charrefs=True)
        self.__link_list = []

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        for attr in attrs:
            if attr[0] == 'href':
                if attr[1] == '' or attr[1] is None:
                    continue
                else:
                    self.__link_list.append(attr[1])

    def get_link_list(self):
        return self.__link_list


def links_poces(links_list: list):

    """
    :param links_list: список url-адресов, найденных на сайте
    :return: Возвращает два списка url-адресов (внутренних и внешних)
    """
    urls_with_same_domain = set()
    urls_with_another_domain = set()

    for link in links_list:

        link = urljoin(HOMEPAGE_URL, link)
        parse_link = urlparse(link)
        netloc = parse_link.netloc.replace('.ru', f'.{DOMEN_ZONE}').replace('.com', f'.{DOMEN_ZONE}')
        full_link = 'https://' + netloc + parse_link.path

        netloc = urlparse(full_link).netloc
        if netloc == DOMEN_NAME_2 or netloc == DOMEN_NAME_1:
            urls_with_same_domain.add(full_link)
        else:
            urls_with_another_domain.add(full_link)

    return urls_with_same_domain, urls_with_another_domain

def get_urls_on_page(url: str):
    global all_urls
    global urls_relation

    if url.endswith('/'):
        url = url[:-1]

    try:
        with urlopen(url) as response:
            html_body = response.read()
            true_full_link = response.geturl()
    except:
        return

    parse_true_link = urlparse(true_full_link)
    netloc = parse_true_link.netloc.replace('.ru', f'.{DOMEN_ZONE}').replace('.com', f'.{DOMEN_ZONE}')
    if netloc != DOMEN_NAME_2 and netloc != DOMEN_NAME_1:
        # url с другим доменом
        all_urls.add(true_full_link)
        return

    if true_full_link in all_urls:
        # уже искал по данному url
        return
    all_urls.add(true_full_link)

    try:
        html_decoded_body = html_body.decode("utf-8")
    except UnicodeDecodeError:
        html_decoded_body = html_body.decode('latin-1')

    LinkSearcher = LinkParser()
    LinkSearcher.feed(html_decoded_body)

    urls_with_same_domain, urls_with_another_domain = links_poces(LinkSearcher.get_link_list())
    urls_relation[url] = urls_with_same_domain.union(urls_with_another_domain)

    for founded_url in urls_with_another_domain:
        # сохраняю url с другим доменом
        all_urls.add(founded_url)

    return urls_with_same_domain

def do_sitemap(url: str):
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

    while(DEFAULT_COUNT_THREADS != len(threading.enumerate())):
        print('Всего активных потоков:', len(threading.enumerate()))
        time.sleep(5)

    print('Потоков стандартное количество')
    end = time.time() - start

    print()
    print('Отчет')
    print(f'URL: {HOMEPAGE_URL}')
    print(f'Время обработки: {int(end)} сек')
    print(f'Количество найденных ссылок: {len(all_urls)} ')

    f = open(r'urllib_results/vk.txt', 'w', encoding="utf-8")
    f.write(f'ОТЧЕТ \n \n')
    f.write(f'URL: {HOMEPAGE_URL} \n')
    f.write(f'Время обработки: {int(end)} \n')
    f.write(f'Количество найденных ссылок: {len(all_urls)} \n \n \n ')
    f.write(f'Список ссылок: \n {all_urls} \n \n \n ')
    f.write(f'Зависимости: \n {urls_relation} \n \n \n ')
    f.close()

    results = (HOMEPAGE_URL, 'urllib', len(all_urls), int(end))
    add_sitemap_creations(results)

    site_nodes = []
    for parent_url in urls_relation:
        for url in urls_relation[parent_url]:
            site_nodes.append((HOMEPAGE_URL, parent_url, url))
    add_sitemaps_links_urllib(site_nodes)
