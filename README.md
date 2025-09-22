# Web Map Service (WMS) Server на Flask и MapScript

## Описание проекта

Проект представляет собой WMS-сервер для отображения картографических данных. Сервер позволяет загружать пары файлов (стиль карты .map и данные .json) в базу данных и затем отображать их через стандартные WMS-запросы.

## Архитектура

- Backend: Flask + Python MapScript
- База данных: SQLite
- Хранение данных: Картостили и GeoJSON данные хранятся в БД
- Временные файлы: Создаются в директории temp/ во время запросов

## Установка и зависимости

Клонируйте репозиторий:

```bash
git clone https://github.com/MikhailKlidzhan/mapscript-project.git
```

Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```

Для Ubuntu/Debian также требуется:

```bash
sudo apt install python3-mapscript
```

## Использование

1. **Инициализация базы данных**

```bash
python3 -c "from database import init_db; init_db()"
```

2. **Загрузка примеров карт**

```bash
# Загрузка карты в системе координат Web Mercator (EPSG:3857)
python3 load_data.py spb3857 spb3857.map spb3857.json

# Загрузка карты в системе координат WGS84 (EPSG:4326)
python3 load_data.py spb4326 spb4326.map spb4326.json
```

3. **Запуск сервера**

```bash
python3 app.py
```

Сервер будет доступен по адресу: http://localhost:3007

4. **Доступные endpoint'ы**

- GET / - список всех загруженных карт
- GET /\<mapname\> - WMS-запрос для конкретной карты

5. **Пример WMS-запроса**

```text
http://localhost:3007/spb3857?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=3359332.801464934368,8381615.12248637341,3377232.975584486965,8395864.989966142923&CRS=EPSG:3857&WIDTH=1016&HEIGHT=808&LAYERS=spb&STYLES=&FORMAT=image/png
```

## Утилита загрузки данных

```bash
python3 load_data.py <mapname> <mapfile> <geojsonfile>
```

Пример:

```bash
python3 load_data.py mymap mymap.map mydata.json
```

## Структура проекта

```text
project/
├── app.py              # Основное Flask приложение
├── database.py         # Модуль работы с БД
├── load_data.py        # Утилита загрузки данных
├── requirements.txt    # Зависимости Python
├── maps.db           # SQLite база данных (создается автоматически)
└── temp/             # Временная директория (создается автоматически)
```
