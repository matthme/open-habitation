import falcon
import json
import functools

from falcon import media
from falcon_apispec import FalconPlugin
from wsgiref.simple_server import make_server
from pandas_datapackage_reader import read_datapackage
from apispec import APISpec
from swagger_ui import falcon_api_doc

app = application = falcon.App()

from api_prototype import *

json_handler = media.JSONHandler(
    dumps=functools.partial(json.dumps, indent=4, sort_keys=True),
)


class ProductionResource:
    def on_get(self, req, resp):
        """Handles GET requests
        ---
        description: Gets building data
        responses:
            200:
                description: JSON blob
        """
        resp.media = yearly_production("Wiesenstrasse", 2, 5200, "Brugg")
        resp.media_handler = json_handler

    def on_post(self, req, resp):
        """Handles POST requests
        ---
        description: Gets building data for a search address
        requestBody:
            required: true
            content:
                application/x-www-form-urlencoded:
                    schema:
                        type: object
                        properties:
                            address:
                                type: string
                                description: Building in Switzerland
        responses:
            200:
                description: JSON blob
        """
        obj = req.get_media()
        address = obj.get('address')
        print(address)
        resp.media = yearly_production(address)
        resp.media_handler = json_handler
        get_production_info_string(address)


prod_res = ProductionResource()
app.add_route("/api/production/yearly", prod_res)


spec = APISpec(
    title="EcoHabitasOpen APP",
    version="0.0.1",
    openapi_version='3.0',
    plugins=[FalconPlugin(app)],
)

spec.path(resource=prod_res)

# BUG! https://github.com/PWZER/swagger-ui-py/issues/29
# falcon_api_doc(app, config=spec.to_dict(), url_prefix='/api/doc', title='API doc')

if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
