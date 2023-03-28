# Sitemap creator
<br />
<br />

 В данном проекте реализованы два скрипта, которые делают карту сайта. Первый написан с использованием библиотеки urllib. Второй с использованием библиотеки requests_html. 
<br />
В папке db создержется база данных (SQLite), которая состоит из двух табличек:
- Результат работы скриптов (кол-во. ссылок, время работы, тип парсера)
- Перечень всех ссылок (с указанием домена и родительской ссылки)

В папках с результатом находятся файлы с подробными итогами прогона скрипта (перечень всех ссылок с указанием родительской ссылки).
<br />
<br />

## Результаты скрипта с использованием requests_html


| URL сайта | Время обработки | Кол-во найденных ссылок | Имя файла с результатом |
| ------ | ------ | ------ | ------ |
| www.google.com/ | 71 | 3297 | requests_html_results/google.txt
| www.crawler-test.com/  | 180 | 640 | requests_html_results/crawler-test.txt
| www.stackoverflow.com/  | 66 | 728 | requests_html_results/stackoverflow.txt
| www.vk.com/  | 116 | 1106 | requests_html_results/vk.txt

<br />
Не удалось создать карту сайта для dzen.com так как сайт блокирует get запросы.
<br />

## Результаты скрипта с использованием urllib


| URL сайта | Время обработки | Кол-во найденных ссылок | Имя файла с результатом |
| ------ | ------ | ------ | ------ |
| www.google.com/ | 65 | 2084 | urllib_results/google.txt
| www.crawler-test.com/  | 111 | 399 | urllib_results/crawler-test.txt
| www.stackoverflow.com/  | 26 | 134 | urllib_results/stackoverflow.txt
