from flask import Flask, request, Response
import mapscript
import os
from database import init_db, get_map_data, get_all_maps


app = Flask(__name__)


class MapServer:
    def __init__(self, mapstyle_content, geojson_content, mapname):
        self.mapstyle_content = mapstyle_content
        self.geojson_content = geojson_content
        self.mapname = mapname

    def render_map(self, query_string):
        # create temp dir
        temp_dir = os.path.abspath("temp")
        os.makedirs(temp_dir, exist_ok=True)

        # save geojson into a tempfile
        geojson_path = os.path.join(temp_dir, f"{self.mapname}.json")
        with open(geojson_path, "w") as f:
            f.write(self.geojson_content)

        # save mapfile into a tempfile
        mapfile_path = os.path.join(temp_dir, f"{self.mapname}.map")
        with open(mapfile_path, "w") as f:
            f.write(self.mapstyle_content)


        try:
            # create map object
            map_obj = mapscript.mapObj(mapfile_path)

            # create and configure query
            ows_request = mapscript.OWSRequest()
            ows_request.loadParamsFromURL(query_string)

            # handle query - get status code
            status_code = map_obj.OWSDispatch(ows_request)
            print(f"OWSDispatch вернул статус: {status_code}")
            
            # on success, create an image
            if status_code == mapscript.MS_SUCCESS:
                # create an image
                image = map_obj.draw()
                
                if image:
                    # get image bytes
                    response_data = image.getBytes()
                    content_type = 'image/png'
                    return response_data, content_type
                else:
                    raise Exception("Не удалось создать изображение")
            else:
                raise Exception(f"Ошибка рендеринга, код: {status_code}")
        
        except Exception as e:
            raise Exception(f"Ошибка при рендеринге карты: {str(e)}")
        
        finally:
            #  delete tempfiles
            try:
                os.remove(geojson_path)
                os.remove(mapfile_path)
            
            except:
                pass


@app.route("/<mapname>", methods=["GET"])
def serve_map(mapname):
    # get query params
    query_string = request.query_string.decode("utf-8")

    # get data from db
    mapstyle_content, geojson_content = get_map_data(mapname)

    if not mapstyle_content or not geojson_content:
        return f"Карта с именем {mapname} не найдена!", 404
    
    # render map
    try:
        map_server = MapServer(mapstyle_content, geojson_content, mapname)
        response_data, content_type = map_server.render_map(query_string)

        print(f"Сгенерировано изображение размером: {len(response_data)} байт")

        if not response_data or len(response_data) == 0:
            return "Не удалось сгенерировать изображение", 500
        
        response = Response(response_data, content_type=content_type)
        response.headers['Content-Disposition'] = 'inline'
        return response
    
    except Exception as e:
        return f"Ошибка: {str(e)}", 500
    

@app.route("/")
def list_maps():
    """Page with all maps available"""
    maps = get_all_maps()

    html = "<h1>Доступные карты</h1><ul>"
    for map_name in maps:
        html += f"<li><a href='/{map_name}?{example_query}'>{map_name}</a></li>"
    html += "</ul>"

    return html

example_query = "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX=3359332.801464934368,8381615.12248637341,3377232.975584486965,8395864.989966142923&CRS=EPSG:3857&WIDTH=1016&HEIGHT=808&LAYERS=spb&STYLES=&FORMAT=image/png"


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=3007, debug=True)


