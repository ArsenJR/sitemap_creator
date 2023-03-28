import sqlite3

def add_sitemap_creations(data):
    db = sqlite3.connect(r'db/sitemaps.db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO sitemaps_creations VALUES (?,?,?,?);", data)
    db.commit()
    db.close()

def add_sitemaps_links_urllib(data):
    db = sqlite3.connect(r'db/sitemaps.db')
    cursor = db.cursor()
    cursor.executemany("INSERT INTO sitemaps_links_urllib VALUES (?,?,?);", data)
    db.commit()
    db.close()

def add_sitemaps_links_requests_html(data):
    db = sqlite3.connect(r'db/sitemaps.db')
    cursor = db.cursor()
    cursor.executemany("INSERT INTO sitemaps_links_requests_html VALUES (?,?,?);", data)
    db.commit()
    db.close()


if __name__ == "__main__":

    db = sqlite3.connect(r'db/sitemaps.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM sitemaps_creations;")
    one_result = cursor.fetchall()
    print(one_result)

    cursor.execute("SELECT * FROM sitemaps_links_urllib;")
    one_result = cursor.fetchall()
    #print(one_result)

    db.close()