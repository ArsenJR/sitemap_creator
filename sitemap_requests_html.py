import threading
import time

from requests_html import HTMLSession

from urllib.parse import urljoin, urlparse

from update_data import add_sitemaps_link_requests_html, get_all_link_by_proc_id, get_proc_id

DEFAULT_COUNT_THREADS = len(threading.enumerate())

def get_urls_on_page(url: str, homepage, domen_name_1, domen_name_2, proc_id, all_links):
    """
        :param url: url адрес
        :return: возвращает список ссылок, найденных на странице
    """



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
        link = urljoin(homepage, link)
        # проверяем доменное имя

        netloc = urlparse(link).netloc
        if netloc == domen_name_1 or netloc == domen_name_2:
            urls_with_same_domain.add(link)
        else:
            urls_with_another_domain.add(link)

        # заполняем новые ссылки в карту сайта
    for founded_url in urls_with_another_domain:
        if founded_url not in all_links:
            # сохраняю url с другим доменом
            add_sitemaps_link_requests_html((proc_id, homepage, url, founded_url))

    for founded_url in urls_with_same_domain:
        if founded_url not in all_links:
            add_sitemaps_link_requests_html((proc_id, homepage, url, founded_url))

    return urls_with_same_domain

def do_sitemap_requests_html(url: str, domen_name_1, domen_name_2, proc_id, table_name, depth=0, homepage=None):
    """
        Сканирует веб-страницу и извлекает все ссылки.
    """
    if not homepage:
        homepage = url
        add_sitemaps_link_requests_html((proc_id, homepage, homepage, homepage))

    all_links = get_all_link_by_proc_id(proc_id, table_name)
    urls_with_same_domain = get_urls_on_page(url, homepage, domen_name_1, domen_name_2, proc_id, all_links)

    if not urls_with_same_domain:
        # подходящих url не найдено на странице
        return

    for founded_url in urls_with_same_domain:
        if founded_url in all_links:
            # url уже рассматривался
            continue

        if depth > 40:
            # привешение лимита
            return
        depth += 1
        print(depth)
        thread = threading.Thread(target=do_sitemap_requests_html, args=(founded_url, domen_name_1, domen_name_2, proc_id, table_name, depth, homepage,))
        thread.start()

    return
if __name__ == "__main__":

    start = time.time()
    homepage = 'https://www.google.com/'
    domen_name_1 = urlparse(homepage).netloc
    domen_name_2 = domen_name_1.replace('www.', '')
    table_name = 'sitemaps_links_requests_html'
    proc_id = get_proc_id(table_name)
    do_sitemap_requests_html(homepage, domen_name_1, domen_name_2, proc_id, table_name)


    print('Слежу за потоками:')
    while (DEFAULT_COUNT_THREADS != len(threading.enumerate())):
        print('Всего активных потоков:', len(threading.enumerate()))
        all_urls = get_all_link_by_proc_id(proc_id, table_name)
        print(f'Количество найденных ссылок: {len(all_urls)} ')
        time.sleep(5)

    print('Потоков стандартное количество')
    end = time.time() - start
    all_urls = get_all_link_by_proc_id(proc_id, table_name)

    print()
    print('Отчет')
    print(f'URL: {homepage}')
    print(f'Время обработки: {int(end)} сек')
    print(f'Количество найденных ссылок: {len(all_urls)} ')

