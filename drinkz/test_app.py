import app
import urllib
from . import db, recipes
import generate_html

def test_WSGI():

    environ = {}
    environ['PATH_INFO'] = '/recipes.html'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status = d['status']
    headers = d['headers']

    assert text.find("scotch on the rocks") != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
