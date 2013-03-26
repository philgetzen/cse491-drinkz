import app
import urllib
from . import db, recipes


def test_WSGI():
    db._reset_db()
    x = list(db.get_all_recipes())
    assert not x                

    r = recipes.Recipe('scotch on the rocks', [('blended scotch',
                                               '4 oz')])

    db.add_recipe(r)

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

    app_obj.recipes( environ, my_start_response)

    assert text.find("scotch on the rocks") != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'
