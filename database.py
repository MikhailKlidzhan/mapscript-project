import sqlite3


def init_db():
    """Database initialization and table creation"""

    conn = sqlite3.connect("maps.db")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS maps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mapname TEXT UNIQUE NOT NULL,
            mapstyle TEXT NOT NULL,
            gjson TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def insert_map_data(mapname, mapstyle_content, geojson_content):
    """Mapdata insertion into database"""

    conn = sqlite3.connect("maps.db")
    c = conn.cursor()

    try:
        c.execute(
            """
            INSERT INTO maps (mapname, mapstyle, gjson) 
            VALUES (?, ?, ?)
            """,
            (mapname, mapstyle_content, geojson_content)
        )
        conn.commit()
        print(f"Данные для {mapname} успешно добавлены в БД")
    except sqlite3.IntegrityError:
        print(f"Карта с именем {mapname} уже существует в БД")
    finally:
        conn.close()


def get_map_data(mapname):
    """Mapdata retrieval from database"""
    conn = sqlite3.connect("maps.db")
    c = conn.cursor()

    c.execute(
        "SELECT mapstyle, gjson FROM maps WHERE mapname = ?",
        (mapname, )
    )

    result = c.fetchone()
    conn.close()

    if result:
        return result[0], result[1]
    else:
        return None, None
    

def get_all_maps():
    """All maps names retrieval from database"""
    conn = sqlite3.connect("maps.db")
    c = conn.cursor()

    c.execute("SELECT mapname FROM maps")
    results = c.fetchall()
    conn.close()

    return [result[0] for result in results]
