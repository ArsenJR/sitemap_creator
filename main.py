import threading
import time

from urllib.parse import urlparse

from update_data import get_proc_id, get_all_link_by_proc_id

from sitemap_urllib import do_sitemap_urllib
from sitemap_requests_html import do_sitemap_requests_html

def save_report_in_txt(path_to_file, data):
    with open(f'{path_to_file}', 'w', encoding="utf-8") as f:
        f.write(f'ОТЧЕТ \n \n')
        f.write(f'URL: {data[0]} \n')
        f.write(f'Время обработки: {data[1]} \n')
        f.write(f'Количество найденных ссылок: {len(data[2])} \n \n \n ')
        f.write(f'Список ссылок: \n {data[2]}')

def do_sitemap(homepage, kind_of_parser):
    """

    """
    start = time.time()
    default_count_threads = len(threading.enumerate())

    results_file_name = homepage.split('.')[-2] + '.txt'

    domen_name_1 = urlparse(homepage).netloc
    domen_name_2 = domen_name_1.replace('www.', '')
    domen_zone = domen_name_1.split('.')[2]

    if kind_of_parser == 1:
        # при помощии urllib
        path_results_file = f'urllib_results/{results_file_name}'
        table_name = 'sitemaps_links_urllib'
        proc_id = get_proc_id(table_name)

        do_sitemap_urllib(homepage, domen_name_1, domen_name_2, domen_zone, proc_id, table_name)


    if kind_of_parser == 2:
        # при помощи requests_html
        path_results_file = f'urllib_results/{results_file_name}'
        table_name = 'sitemaps_links_requests_html'
        proc_id = get_proc_id(table_name)

        do_sitemap_requests_html(homepage, domen_name_1, domen_name_2, proc_id, table_name)


    while (default_count_threads != len(threading.enumerate())):
        print('Всего активных потоков:', len(threading.enumerate()))
        all_urls = get_all_link_by_proc_id(proc_id, table_name)
        print(f'Количество найденных ссылок: {len(all_urls)} ')
        print()
        time.sleep(5)

    print('Потоков стандартное количество')
    end = time.time() - start

    all_urls = get_all_link_by_proc_id(proc_id, table_name)

    print()
    print('Отчет')
    print(f'URL: {homepage}')
    print(f'Время обработки: {int(end)} сек')
    print(f'Количество найденных ссылок: {len(all_urls)} ')

    save_report_in_txt(path_results_file, [homepage, int(end), all_urls])



if __name__ == "__main__":
    url_for_search = input('URL to do sitemap: ')

    parser_type = int(input('Wich kind of parser 1 - urllib, 2 - requests_html: '))
    print(url_for_search)
    print(parser_type)

    do_sitemap(homepage=url_for_search, kind_of_parser=parser_type)