import sqlite3
import logging

logger = logging.getLogger(__name__)

def init_db():
    """Database initialization and table creation"""
    try: 
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
        logger.info("База данных инициализирована успешно")

    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        raise


def insert_map_data(mapname, mapstyle_content, geojson_content):
    """Mapdata insertion into database"""
    try:
        conn = sqlite3.connect("maps.db")
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO maps (mapname, mapstyle, gjson) 
            VALUES (?, ?, ?)
            """,
            (mapname, mapstyle_content, geojson_content)
        )
        conn.commit()
        logger.info(f"Данные для {mapname} успешно добавлены в БД")
    except sqlite3.IntegrityError:
        logger.warning(f"Карта с именем {mapname} уже существует в БД")
    except Exception as e:
        logger.error(f"Ошибка при добавлении данных в БД: {e}")
        raise
    finally:
        conn.close()


def get_map_data(mapname):
    """Mapdata retrieval from database"""
    try:
        conn = sqlite3.connect("maps.db")
        c = conn.cursor()

        c.execute(
            "SELECT mapstyle, gjson FROM maps WHERE mapname = ?",
            (mapname, )
        )

        result = c.fetchone()

        if result:
            logger.debug(f"Данные для карты {mapname} найдены в БД")
            return result[0], result[1]
        else:
            logger.debug(f"Данные для карты {mapname} не найдены в БД")
            return None, None
        
    except Exception as e:
        logger.error(f"Ошибка при получении данных из БД: {e}")
        return None, None
    
    finally:
        conn.close()


def get_all_maps():
    """All maps names retrieval from database"""
    try:
        conn = sqlite3.connect("maps.db")
        c = conn.cursor()

        c.execute("SELECT mapname FROM maps")
        results = c.fetchall()

        logger.debug(f"Найдено {len(results)} карт в БД")
        return [result[0] for result in results]
    
    except Exception as e:
        logger.error(f"Ошибка при получении списка карт: {e}")
        return []
    
    finally:
        conn.close()
