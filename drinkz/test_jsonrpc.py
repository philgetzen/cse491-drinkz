import app
import urllib
from StringIO import StringIO
from . import db, recipes
import generate_html
import simplejson


def jsonrpc(method, params):
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    environ['wsgi.input'] = StringIO(simplejson.dumps({
        'method': method,
        'params': params,
        'id': 1
    }))
    environ['CONTENT_LENGTH'] = len(environ['wsgi.input'].getvalue())

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    status = d['status']
    headers = d['headers']
    result_dict =  simplejson.loads(''.join(results))

    return (status, headers, result_dict)

def test_convert_units_to_ml():
    status, headers, result = jsonrpc('convert_units_to_ml', ['10 oz'])

    assert result['result'] == 295.735, result['result']
    assert ('Content-Type', 'application/json') in headers, headers
    assert status == '200 OK'

def test_get_recipe_names():
    status, headers, result = jsonrpc('get_recipe_names', [])

    assert 'scotch on the rocks' in result['result'], result['result']
    assert 'vodka martini' in result['result'], result['result']
    assert ('Content-Type', 'application/json') in headers, headers
    assert status == '200 OK'

def test_get_liquor_inventory():
    status, headers, result = jsonrpc('get_liquor_inventory', [])

    assert 'Gray Goose' in result['result'], result['result']
    assert 'Johnnie Walker' in result['result'], result['result']
    assert 'Uncle Herman\'s' in result['result'], result['result']
    assert 'Rossi' in result['result'], result['result']
    assert ('Content-Type', 'application/json') in headers, headers
    assert status == '200 OK'

def test_add_liquor_type():
    status, headers, result = jsonrpc('add_liquor_type', ['Val Kilmer', 'Pineapple Label', 'Absinthe'])
    assert  result['result'] == True, result['result']

def test_add_liquor_inventory():
    status, headers, result = jsonrpc('add_liquor_type', ['Val Kilmer', 'Pineapple Label', 'Absinthe'])
    status, headers, result = jsonrpc('add_liquor_inventory', ['Val Kilmer', 'Pineapple Label', '200 ml'])
    assert result['result'] == True, result['result']

def test_add_recipe():
    status, headers, result = jsonrpc('add_recipe', ['dumb', '[(stupid, 20 oz)]'])
    assert result['result'] ==  True, result['result']
