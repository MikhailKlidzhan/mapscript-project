import re
import os
import sys
from database import init_db, insert_map_data
import logging

logger = logging.getLogger(__name__)


def modify_map_connection(map_content, mapname, temp_dir):
    """CONNECTION modification in map file"""
    try:
        pattern = r'(CONNECTION\s+")[^"]+(")'
        replacement = fr'\1{temp_dir}/{mapname}.json\2'

        logger.debug(f"Модифицирован CONNECTION для {mapname}")
        return re.sub(pattern, replacement, map_content)
    
    except Exception as e:
        logger.error(f"Ошибка при модификации CONNECTION: {e}")
        raise


def load_map_to_db(mapname, mapfile_path, geojson_path):
    """Pair map+geojson database loading"""
    try:
        # check if files exist
        if not os.path.exists(mapfile_path):
            logger.error(f"Файл {mapfile_path} не найден!")
            return False
        
        if not os.path.exists(geojson_path):
            logger.error(f"Файл {geojson_path} не найден!")
            return False
        
        # read files
        with open(mapfile_path, "r") as f:
            map_content = f.read()

        with open(geojson_path, "r") as f:
            geojson_content = f.read()

        # create temp dir if not exists
        temp_dir = os.path.abspath("temp")
        os.makedirs(temp_dir, exist_ok=True)
        logger.debug(f"Создана временная директория: {temp_dir}")

        # modify map file
        modified_map_content = modify_map_connection(map_content, mapname, temp_dir)

        # save to db
        insert_map_data(mapname, modified_map_content, geojson_content)

        logger.info(f"Данные для {mapname} успешно загружены в БД")
        return True
    
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {e}")
        return False


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )

    init_db()

    if len(sys.argv) != 4:
        logger.error("Неверное количество аргументов. Использование: python3 load_data.py <mapname> <mapfile> <geojsonfile>")
        sys.exit(1)

    mapname = sys.argv[1]
    mapfile = sys.argv[2]
    geojsonfile = sys.argv[3]

    logger.info(f"Начало загрузки данных для {mapname}")

    if load_map_to_db(mapname, mapfile, geojsonfile):
        logger.info("Данные успешно загружены!")
    else:
        logger.error("Ошибка при загрузке данных!")
        sys.exit(1)