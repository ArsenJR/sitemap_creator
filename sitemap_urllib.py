import threading
import time

from html.parser import HTMLParser

from urllib.parse import urlparse, urljoin
from urllib.request import urlopen

from update_data import add_sitemaps_link_urllib, get_all_link_by_proc_id


DEFAULT_COUNT_THREADS = len(threading.enumerate())




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


def links_proces(links_list: list, homepage, domen_name_1, domen_name_2, domen_zone):

    """
    :param links_list: список url-адресов, найденных на сайте
    :return: Возвращает два списка url-адресов (внутренних и внешних)
    """
    urls_with_same_domain = set()
    urls_with_another_domain = set()

    for link in links_list:

        link = urljoin(homepage, link)
        parse_link = urlparse(link)
        netloc = parse_link.netloc.replace('.ru', f'.{domen_zone}').replace('.com', f'.{domen_zone}')
        full_link = 'https://' + netloc + parse_link.path

        netloc = urlparse(full_link).netloc

        if netloc == domen_name_1 or netloc == domen_name_2:
            urls_with_same_domain.add(full_link)
        else:
            urls_with_another_domain.add(full_link)

    return urls_with_same_domain, urls_with_another_domain

def get_urls_on_page(url: str, homepage, domen_name_1, domen_name_2, domen_zone, proc_id, table_name, all_links):

    """
    :param url: url адрес
    :return: возвращает список ссылок, найденных на странице
    """

    if url.endswith('/'):
        url = url[:-1]

    try:
        with urlopen(url) as response:
            html_body = response.read()
            true_full_link = response.geturl()
    except:
        return

    parse_true_link = urlparse(true_full_link)
    netloc = parse_true_link.netloc.replace('.ru', f'.{domen_zone}').replace('.com', f'.{domen_zone}')
    if netloc != domen_name_1 and netloc != domen_name_2:
        # url с другим доменом
        add_sitemaps_link_urllib((proc_id, homepage, url, true_full_link))
        return

    if true_full_link in all_links:
        # уже искал по данному url
        return

    add_sitemaps_link_urllib((proc_id, homepage, url, true_full_link))

    try:
        html_decoded_body = html_body.decode("utf-8")
    except UnicodeDecodeError:
        html_decoded_body = html_body.decode('latin-1')

    LinkSearcher = LinkParser()
    LinkSearcher.feed(html_decoded_body)

    urls_with_same_domain, urls_with_another_domain = links_proces(LinkSearcher.get_link_list(), homepage, domen_name_1, domen_name_2, domen_zone)

    for founded_url in urls_with_another_domain:
        # сохраняю url с другим доменом
        add_sitemaps_link_urllib((proc_id, homepage, url, founded_url))

    return urls_with_same_domain

def do_sitemap_urllib(url: str, domen_name_1, domen_name_2, domen_zone, proc_id, table_name, depth = 0, homepage=None):
    """
    Сканирует веб-страницу и извлекает все ссылки.
    """
    if not homepage:
        homepage = url
        add_sitemaps_link_urllib((proc_id, homepage, homepage, homepage))

    all_links = get_all_link_by_proc_id(proc_id, table_name)
    urls_with_same_domain = get_urls_on_page(url, homepage, domen_name_1, domen_name_2, domen_zone, proc_id, table_name, all_links)


    if not urls_with_same_domain:
        # подходящих url не найдено на странице
        return

    for founded_url in urls_with_same_domain:
        if founded_url in all_links:
            # url уже рассматривался
            continue

        if depth > 60: # максимальня глкбина ветки
            # привешение лимита
            return
        depth += 1
        print(depth)
        thread = threading.Thread(target=do_sitemap_urllib, args=(founded_url, domen_name_1, domen_name_2, domen_zone, proc_id, table_name, depth, homepage, ))
        thread.start()
    return


if __name__ == "__main__":

    start = time.time()
    homepage = 'https://www.google.com'
    domen_name_1 = urlparse(homepage).netloc
    domen_name_2 = domen_name_1.replace('www.', '')
    domen_zone = domen_name_1.split('.')[2]
    proc_id = 6
    table_name = 'sitemaps_links_urllib'
    do_sitemap_urllib(homepage, domen_name_1, domen_name_2, domen_zone, proc_id, table_name)


    print('Слежу за потоками:')

    while(DEFAULT_COUNT_THREADS != len(threading.enumerate())):
        print('Всего активных потоков:', len(threading.enumerate()))
        time.sleep(5)

    print('Потоков стандартное количество')
    end = time.time() - start
    proc_id = 6
    table_name = 'sitemaps_links_urllib'
    all_urls = get_all_link_by_proc_id(proc_id, table_name)

    print()
    print('Отчет')
    print(f'URL: {homepage}')
    print(f'Время обработки: {int(end)} сек')
    print(f'Количество найденных ссылок: {len(all_urls)} ')



