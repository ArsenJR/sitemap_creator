import sqlite3

db = sqlite3.connect(r'db/sitemaps.db')
# создание курсора
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sitemaps_creations ( 
    homepage TEXT,
    parser TEXT,
    count_urls INT,
    proc_time INT
)
""")
db.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sitemaps_links_urllib (
    homepage TEXT,
    paren_link TEXT,
    link TEXT
)
""")
db.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sitemaps_links_requests_html (
    homepage TEXT,
    paren_link TEXT,
    link TEXT
)
""")
db.commit()

db.close()

