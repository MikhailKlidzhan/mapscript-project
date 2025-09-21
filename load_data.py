import re
import os
import sys
from database import init_db, insert_map_data


def modify_map_connection(map_content, mapname, temp_dir):
    """CONNECTION modification in map file"""
    pattern = r'(CONNECTION\s+")[^"]+(")'
    replacement = fr'\1{temp_dir}/{mapname}.json\2'

    return re.sub(pattern, replacement, map_content)


def load_map_to_db(mapname, mapfile_path, geojson_path):
    """Pair map+geojson database loading"""

    # check if files exist
    if not os.path.exists(mapfile_path):
        print(f"Файл {mapfile_path} не найден!")
        return False
    
    if not os.path.exists(geojson_path):
        print(f"Файл {geojson_path} не найден!")
        return False
    
    # read files
    with open(mapfile_path, "r") as f:
        map_content = f.read()

    with open(geojson_path, "r") as f:
        geojson_content = f.read()

    # create temp dir if not exists
    temp_dir = os.path.abspath("temp")
    os.makedirs(temp_dir, exist_ok=True)

    # modify map file
    modified_map_content = modify_map_connection(map_content, mapname, temp_dir)

    # save to db
    insert_map_data(mapname, modified_map_content, geojson_content)

    return True


if __name__ == "__main__":
    init_db()

    if len(sys.argv) != 4:
        print("Использование: python load_data.py <mapname> <mapfile> <geojsonfile>")
        print("Пример: python load_data.py spb3857 spb3857.map spb3857.json")
        sys.exit(1)

    mapname = sys.argv[1]
    mapfile = sys.argv[2]
    geojsonfile = sys.argv[3]

    if load_map_to_db(mapname, mapfile, geojsonfile):
        print("Данные успешно загружены!")
    else:
        print("Ошибка при загрузке данных!")