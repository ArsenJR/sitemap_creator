import sqlite3

def add_sitemaps_link_urllib(data):
    with sqlite3.connect(r'db/sitemaps.db', timeout=40) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO sitemaps_links_urllib VALUES (?,?,?,?);", data)

def add_sitemaps_link_requests_html(data):
    with sqlite3.connect(r'db/sitemaps.db', timeout=40) as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO sitemaps_links_requests_html VALUES (?,?,?,?);", data)

def get_all_link_by_proc_id(proc_id: int, table_name: str):
    with sqlite3.connect(r'db/sitemaps.db', timeout=40) as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT DISTINCT link FROM {table_name} WHERE id_proc={proc_id};")
        result = cursor.fetchall()
        all_links = set()
        for link in result:
            all_links.add(link[0])

        return all_links

def get_proc_id(table_name):
    with sqlite3.connect(r'db/sitemaps.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT DISTINCT id_proc FROM {table_name};")
        result = cursor.fetchall()
        if not result:
            return 1
        last_id = 1
        for row in result:
            if last_id < int(row[0]):
                last_id = int(row[0])

        return last_id+1


if __name__ == "__main__":
    with sqlite3.connect(r'db/sitemaps.db') as db:
        cursor = db.cursor()
        cursor.execute(f"SELECT DISTINCT link FROM sitemaps_links_urllib WHERE id_proc=16;")
        result = cursor.fetchall()
        print(len(result))
        print(result)