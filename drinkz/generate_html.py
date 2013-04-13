#!/usr/bin/env python

from os import mkdir, path

from jinja2 import Environment, PackageLoader

import db
import recipes
import urllib2

try:
    mkdir('html')
except OSError:
    # already exists
    pass

base_dir = path.realpath(path.dirname(path.realpath(__file__)) + '/../')
print base_dir
env = Environment(loader=PackageLoader('drinkz', 'tmpl'))

####################################################
#Create Data
####################################################

def create_data():
    try:
        db.load_db('database')
    except Exception:
        db._reset_db()

        db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
        db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

        db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
        db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

        db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
        db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

        db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
        db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

        r = recipes.Recipe('scotch on the rocks', [('blended scotch', '2 oz')])
        r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'), ('vermouth', '1.5 oz')])
        db.add_recipe(r)
        db.add_recipe(r2)
        

####################################################
#Index
####################################################

def generate_index():
    data = generate_index_html()
    fp = open('html/index.html', 'w')
    print >>fp, data
    fp.close()


def generate_index_html():
    return env.get_template('index.tmpl').render().encode('ascii', 'ignore')


####################################################
#Recipes
####################################################

def generate_recipes():
    data = generate_recipes_html()
    fp = open('html/recipes.html', 'w')
    print >>fp, data
    fp.close()


def generate_recipes_html():
    return env.get_template('recipes.tmpl').render(db=db._recipes_db).encode('ascii', 'ignore')


####################################################
#Inventory
####################################################

def generate_inventory():
    data = generate_recipes_html()
    fp = open('html/inventory.html', 'w')
    print >>fp, data
    fp.close()


def generate_inventory_html():
    return env.get_template('inventory.tmpl').render(db=db, inventory=db._inventory_db).encode('ascii', 'ignore')

####################################################
#Liquor Types
####################################################

def generate_liquor_types():
    data = generate_liquor_types_html()
    fp = open('html/liquor_types.html', 'w')
    print >>fp, data
    fp.close()


def generate_liquor_types_html():
    return env.get_template('liquor_types.tmpl').render(liquor_types=db._bottle_types_db).encode('ascii', 'ignore')


####################################################
#Conversion Form
####################################################
def generate_conversion_form():
    data = generate_conversion_form_html()
    fp = open('html/convert.html', 'w')
    print >>fp, data
    fp.close()


def generate_conversion_form_html():
    return env.get_template('conversion_form.tmpl').render().encode('ascii', 'ignore')

####################################################
#Conversion Response
####################################################
def generate_conversion_result():
    data = generate_conversion_form_html()
    fp = open('html/convert_result.html', 'w')
    print >>fp, data
    fp.close()


def generate_conversion_result_html():
    return env.get_template('conversion_result.tmpl').render(results=db._tmp_results).encode('ascii', 'ignore')

####################################################
#Add Liquor Type Form
####################################################
def generate_liquor_type_form():
    data = generate_liquor_type_form_html()
    fp = open('html/liquor_types.html', 'w')
    print >>fp, data
    fp.close()


def generate_liquor_type_form_html():
    return env.get_template('liquor_type_form.tmpl').render().encode('ascii', 'ignore')

####################################################
#Add Liquor Type Response
####################################################
def generate_liquor_type_result():
    data = generate_liquor_type_form_html()
    fp = open('html/liquor_type_result.html', 'w')
    print >>fp, data
    fp.close()


def generate_liquor_type_result_html():
    return env.get_template('liquor_type_result.tmpl').render(results=db._tmp_results).encode('ascii', 'ignore')

####################################################
#Add Liquor Inventory Form
####################################################
def generate_liquor_inventory_form():
    data = generate_liquor_inventory_form_html()
    fp = open('html/liquor_inventory.html', 'w')
    print >>fp, data
    fp.close()


def generate_liquor_inventory_form_html():
    return env.get_template('liquor_inventory_form.tmpl').render(quote=urllib2.quote, bottle_types=db._bottle_types_db).encode('ascii', 'ignore')

####################################################
#Add Liquor Inventory Response
####################################################
def generate_liquor_inventory_result():
    data = generate_liquor_inventory_form_html()
    fp = open('html/liquor_inventory_result.html', 'w')
    print >>fp, data
    fp.close()


def generate_liquor_inventory_result_html():
    return env.get_template('liquor_inventory_result.tmpl').render(unquote=urllib2.unquote, results=db._tmp_results).encode('ascii', 'ignore')

####################################################
#Add Recipe Form
####################################################
def generate_recipe_form():
    data = generate_recipe_form_html()
    fp = open('html/recipe.html', 'w')
    print >>fp, data
    fp.close()


def generate_recipe_form_html():
    return env.get_template('recipe_form.tmpl').render(bottle_types=db._bottle_types_db).encode('ascii', 'ignore')

####################################################
#Add Recipe Response
####################################################
def generate_recipe_result():
    data = generate_recipe_form_html()
    fp = open('html/recipe_result.html', 'w')
    print >>fp, data
    fp.close()


def generate_recipe_result_html():
    return env.get_template('recipe_result_form.tmpl').render(results=db._tmp_results).encode('ascii', 'ignore')
