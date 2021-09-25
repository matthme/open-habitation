import falcon
import json
import functools

from falcon import media
from wsgiref.simple_server import make_server
from pandas_datapackage_reader import read_datapackage
from apispec import APISpec
from falcon_apispec import FalconPlugin

app = application = falcon.App()


from api_prototype import *


data = read_datapackage(".")


def get_paginated_json(req, df):
    per_page = int(req.get_param('per_page', required=False, default=10))
    page = (int(req.get_param('page', required=False, default=1))-1)*per_page
    return df[page:page+per_page].to_json(orient='records')


class TreeResource:
    def __init__(self, data):
        self.trees = data

    def on_get(self, req, resp):
        df = self.trees.copy()
        for fld in self.trees._metadata['schema']['fields']:
            fn = fld['name']
            q = req.get_param(fn, None)
            if q is not None:
                try:
                    q = q.strip()
                    q = int(q)
                    df = df.loc[df[fn] == q]
                except:
                    pass

        resp.status = falcon.HTTP_200
        resp.body = get_paginated_json(req, df)


app.add_route('/tree', TreeResource(data))


class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests
        ---
        description: Prints cite from Kant
        responses:
            200:
                description: Cite to be returned
        """
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')
        resp.content_type = falcon.MEDIA_TEXT


things = ThingsResource()
app.add_route("/things", things)


json_handler = media.JSONHandler(
    dumps=functools.partial(json.dumps, indent=4, sort_keys=True),
)


class BuildingResource:
    def on_get(self, req, resp):
        """Handles GET requests
        ---
        description: Gets building data
        responses:
            200:
                description: JSON blob
        """
        resp.media = get_production_info("Wiesenstrasse", 2, 5200, "Brugg")
        resp.media_handler = json_handler


bldgs = BuildingResource()
app.add_route("/bldgs", bldgs)


spec = APISpec(
    title="Things APP",
    version="0.0.1",
    openapi_version='3.0',
    plugins=[FalconPlugin(app)],
)

spec.path(resource=bldgs)
print(spec.to_yaml())

if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
