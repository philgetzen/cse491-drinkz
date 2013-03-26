#! /usr/bin/env python

from os import mkdir, path
import drinkz.db
from drinkz import recipes

try:
    mkdir('html')
except OSError:
    # already exists
    pass

base_dir = path.realpath(path.dirname(path.realpath(__file__)) + '/../')

####################################################
#Create Data
####################################################


def create_data():
    try:
        drinkz.db.load_db('database')
    except Exception:
        drinkz.db._reset_db()

        drinkz.db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
        drinkz.db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

        drinkz.db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
        drinkz.db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

        drinkz.db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
        drinkz.db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

        drinkz.db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
        drinkz.db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

        r = recipes.Recipe('scotch on the rocks', [('blended scotch', '2 oz')])
        r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'), ('vermouth', '1.5 oz')])
        drinkz.db.add_recipe(r)
        drinkz.db.add_recipe(r2)

####################################################
#Header/Footer nonsense
####################################################

def load_header_footer():
    header = open(base_dir + '/html/header.html').read()
    footer = open(base_dir + '/html/footer.html').read()

    return (header, footer)


####################################################
#Index
####################################################


def generate_index():
    data = generate_index_html()
    fp = open('html/index.html', 'w')
    print >>fp, data
    fp.close()


def generate_index_html():
    header, footer = load_header_footer()
    data = """\
    <div class="row-fluid">
        <div class="hero-unit">
            <h1>can i haz drinkz?</h1>
        </div>
    </div>
    """

    return header + data + footer


####################################################
#Recipes
####################################################

def generate_recipes():
    data = generate_recipes_html()
    fp = open('html/recipes.html', 'w')
    print >>fp, data
    fp.close()


def generate_recipes_html():
    header, footer = load_header_footer()
    data = """\
    <div class="row-fluid">
        <div class="hero-unit">
            <h2>Available Recipes</h2>
            <ul>
    """

    for r in drinkz.db._recipes_db:
        data += "<li>"
        data += r.name + "&#151;"
        if r.need_ingredients() == []:
            data += "Yes"
        else:
            data += "No"
        data += "</li>"

    data += """\
            </ul>
        </div>
    </div>
    """
    
    return header + data + footer

####################################################
#Inventory
####################################################

def generate_inventory():
    data = generate_recipes_html()
    fp = open('html/inventory.html', 'w')
    print >>fp, data
    fp.close()


def generate_inventory_html():
    header, footer = load_header_footer()
    data = """\
    <div class="row-fluid">
        <div class="hero-unit">
            <h2>Available Liquor Amounts</h2>
            <ul>
    """

    for (mfg, liquor) in drinkz.db._inventory_db:
        amount = drinkz.db.get_liquor_amount(mfg, liquor)
        data += "<li>"
        data += mfg + "&#151;" + liquor + "&#151;" + str(amount)
        data += "</li>"

    data += """\
            </ul>
        </div>
    </div>
    """
    
    return header + data + footer


####################################################
#Liquor Types
####################################################

def generate_liquor_types():
    data = generate_liquor_types_html()
    fp = open('html/liquor_types.html', 'w')
    print >>fp, data
    fp.close()


def generate_liquor_types_html():
    header, footer = load_header_footer()
    data = """\
    <div class="row-fluid">
        <div class="hero-unit">
            <h2>Available Liquor Types</h2>
            <ul>
    """

    for (mfg, lqr, typ) in drinkz.db._bottle_types_db:
        data +="<li>"
        data += mfg + "&#151;" + lqr + "&#151;" + typ

    data += """\
            </ul>
        </div>
    </div>
    """

    return header + data + footer
