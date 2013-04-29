#! /usr/bin/env python
# from wsgiref.simple_server import make_server

import generate_html

import urlparse
import simplejson
import db
from os import path

import urllib2
import recipes
import convert

dispatch = {
    '/' : 'index',
    '/recipes.html' : 'recipes',
    '/inventory.html' : 'inventory',
    '/liquor_types.html' : 'liquor_types',
    '/convert.html' : 'conversion_tool',
    '/liquor_type_form.html' : 'liquor_type_form',
    '/liquor_inventory_form.html' : 'liquor_inventory_form',
    '/recipe_form.html' : 'recipe_form',
    '/css/bootstrap.css': 'bootstrap_css',
    '/css/bootstrap-responsive.css': 'bootstrap_responsive_css',
    '/js/bootstrap.js': 'bootstrap_js',
    '/img/glyphicons-halflings.png': 'glyphicons_halflings',
    '/img/glyphicons-halflings-white.png': 'glyphicons_halflings_white',
    '/recv_conversion' : 'recv_conversion',
    '/recv_liquor_type' : 'recv_liquor_type',
    '/recv_liquor_inventory' : 'recv_liquor_inventory',
    '/recv_recipe' : 'recv_recipe',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc'
}

html_headers = [('Content-type', 'text/html')]
css_headers = [('Content-type', 'text/css')]
js_headers = [('Content-type', 'text/javascript')]
png_headers = [('Content-type', 'image/png')]

base_dir = path.realpath(path.dirname(path.realpath(__file__)) + '/../')
firstRun = True

class SimpleApp(object):
    def __call__(self, environ, start_response):
        global firstRun
        if firstRun:
            generate_html.create_data()
            firstRun = False

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = generate_html.generate_index_html()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        data = generate_html.generate_recipes_html()
        start_response('200 OK', list(html_headers))
        return[data]

    def inventory(self, environ, start_response):
        data = generate_html.generate_inventory_html()
        start_response('200 OK', list(html_headers))
        return[data]

    def liquor_types(self, environ, start_response):
        data = generate_html.generate_liquor_types_html()
        start_response('200 OK', list(html_headers))
        return[data]

    def conversion_tool(self, environ, start_response):
        data = generate_html.generate_conversion_form_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def liquor_type_form(self, environ, start_response):
        data = generate_html.generate_liquor_type_form_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def liquor_inventory_form(self, environ, start_response):
        data = generate_html.generate_liquor_inventory_form_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def recipe_form(self, environ, start_response):
        data = generate_html.generate_recipe_form_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def bootstrap_css(self, environ, start_response):
        data = open(base_dir + '/css/bootstrap.css').read()
        start_response('200 OK', list(css_headers))
        return [data]

    def bootstrap_responsive_css(self, environ, start_response):
        data = open(base_dir + '/css/bootstrap-responsive.css').read()
        start_response('200 OK', list(css_headers))
        return [data]

    def bootstrap_js(self, environ, start_response):
        data = open(base_dir + '/js/bootstrap.js').read()
        start_response('200 OK', list(js_headers))
        return [data]

    def glyphicons_halflings(self, environ, start_response):
        data = open(base_dir + '/img/glyphicons-halflings.png', 'rb').read()
        start_response('200 OK', list(png_headers))
        return [data]

    def glyphicons_halflings_white(self, environ, start_response):
        data = open(base_dir + '/img/glyphicons-halflings-white.png', 'rb').read()
        start_response('200 OK', list(png_headers))
        return [data]

    def somefile(self, environ, start_response):
        data = open('somefile.html').read()
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
        start_response('200 OK', list(html_headers))
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()
        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()
        start_response('200 OK', list(html_headers))
        return [data]

    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_conversion(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['amount'][0]
        unit = results['unit'][0]

        amount_converted = convert.convert_to_ml(amount + " " + unit)

        db._tmp_results = []

        db._tmp_results.append(amount)
        db._tmp_results.append(unit)
        db._tmp_results.append(amount_converted)

        content_type = 'text/html'
        data = generate_html.generate_conversion_result_html()

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_liquor_type(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        manufacturer = results['manufacturer'][0]
        liquor = results['liquor'][0]
        typ  = results['type'][0]

        db._tmp_results = []

        db._tmp_results.append(manufacturer)
        db._tmp_results.append(liquor)
        db._tmp_results.append(typ)

        db.add_bottle_type(manufacturer, liquor, typ)

        content_type = 'text/html'
        data = generate_html.generate_liquor_type_result_html()

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_liquor_inventory(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        db._tmp_results = []

        liquor = urllib2.unquote(results['liquor'][0])
        strings = liquor.split('~')
        mfg = strings[0]
        liquor = strings[1]
        amount = results['amount'][0]
        unit = results['unit'][0]

        db._tmp_results.append(mfg)
        db._tmp_results.append(liquor)
        db._tmp_results.append(amount + ' ' + unit)

        content_type = 'text/html'
        data = generate_html.generate_liquor_inventory_result_html()
        db.add_to_inventory(mfg, liquor, amount + ' ' + unit)

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_recipe(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata, True)

        typ = []
        amount = []
        unit = []
        ingredients = []

        db._tmp_results = []

        name = results['name'][0]

        for i in range(10):
            typStr = "typ" + str(i)
            amountStr = "amount" + str(i)
            unitStr = "unit" + str(i)
            typ.append(results[typStr][0])
            amount.append(results[amountStr][0])
            unit.append(results[unitStr][0])

        for i in range(10):
            if typ[i] == "" or amount[i] == "":
                continue
            else:
                ingredients.append((typ[i], amount[i] + ' ' + unit[i]))
        r = recipes.Recipe(name, ingredients)
        db.add_recipe(r)

        db._tmp_results.append(name)
        db._tmp_results.append(ingredients)

        content_type = 'text/html'
        data = generate_html.generate_recipe_result_html()

        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                print "Length: ", length
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)

    def rpc_convert_units_to_ml(self, amount):
        return convert.convert_to_ml(amount)

    def rpc_get_recipe_names(self):
        return list(db.get_all_recipes_by_name())

    def rpc_get_liquor_inventory(self):
        return dict(db.get_liquor_inventory())

    def rpc_add_liquor_type(self, mfg, liquor, typ):
        db.add_bottle_type(mfg, liquor, typ)
        return (mfg, liquor, typ) in db._bottle_types_db

    def rpc_add_liquor_inventory(self, mfg, liquor, amount):
        db.add_to_inventory(mfg, liquor, amount)
        return (mfg, liquor) in db._inventory_db

    def rpc_add_recipe(self, name, Ingredients):
        r = recipes.Recipe(name, Ingredients)
        db.add_recipe(r)
        return r in db._recipes_db


def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

def recipe_result(name, typ, amount, unit):
    header, footer = generate_html.load_header_footer()

    data = """\
    <div class="row-fluid">
        <div class="hero-unit">
        <h2>Recipe Added: </h2>
        <h4>Name: </h4>
    """
    data += name
    data += """<h4>Ingredients: </h4><h6>Bottle Type: </h6>"""
    data += """\
            <p><a href="/" class="btn btn-primary btn-large" style="margin-top: 2em;">Return to Home</a></p>
        </div>
    </div>
    """

    return header + data + footer