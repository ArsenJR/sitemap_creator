import sqlite3

with sqlite3.connect(r'db/sitemaps.db') as db:
    # создание курсора
    db.execute("PRAGMA journal_mode=WAL")
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sitemaps_creations ( 
        homepage TEXT,
        parser TEXT,
        count_urls INT,
        proc_time INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sitemaps_links_urllib (
        id_proc INT,
        homepage TEXT,
        paren_link TEXT,
        link TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sitemaps_links_requests_html (
        id_proc INT,
        homepage TEXT,
        paren_link TEXT,
        link TEXT
    )
    """)

