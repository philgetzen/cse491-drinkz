#! /usr/bin/env python

import os
import drinkz.db
from drinkz import recipes

try:
    os.mkdir('html')
except OSError:
    # already exists
    pass

####################################################
#Create Data
####################################################

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
r2 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),
                                            ('vermouth', '1.5 oz')])
drinkz.db.add_recipe(r)
drinkz.db.add_recipe(r2)

####################################################
#Index
####################################################


def generate_index(data):
    data = generate_index_links()
    fp = open('html/index.html', 'w')
    print >>fp, data
    fp.close()


def generate_index_links():
    data = """\
    Visit:
    <p><a href='recipes.html'>Recipes</a>,
    <p><a href='inventory.html'>Inventory</a>,
    <p><a href='liquor_types.html'>Liquor Types</a>
    """
    return data


####################################################
#Recipes
####################################################

fp = open('html/recipes.html', 'w')
print >>fp, "<p><a href='index.html'>Home</a>"
print >>fp, "<p><a href='inventory.html'>Inventory</a>"
print >>fp, "<p><a href='liquor_types.html'>Liquor Types</a>"

print >>fp, """<h3>Available Recipes</h3>"""

print >>fp, "<ul>"
for r in drinkz.db._recipes_db:
	print >>fp, "<li>"
	print >>fp, r.name, "&#151;",
	if r.need_ingredients() == []:
		print >>fp, "Yes"
	else:
		print >>fp, "No"
	print >>fp, "</li>"
print >>fp, "</ul>"

fp.close()

####################################################
#Inventory
####################################################

fp = open('html/inventory.html', 'w')
print >>fp, "<p><a href='index.html'>Home</a>"
print >>fp, "<p><a href='recipes.html'>Recipes</a>"
print >>fp, "<p><a href='liquor_types.html'>Liquor Types</a>"

print >>fp, """<h3>Available Liquor Amounts</h3>"""

print >>fp, "<ul>"
for (mfg, liquor) in drinkz.db._inventory_db:
	amount = drinkz.db.get_liquor_amount(mfg, liquor)
	print >>fp, "<li>"
	print >>fp, mfg, "&#151;", liquor, "&#151;", amount
	print >>fp, "</li>"
print >>fp, "</ul>"
fp.close()


####################################################
#Liquor Types
####################################################

fp = open('html/liquor_types.html', 'w')
print >>fp, "<p><a href='index.html'>Home</a>"
print >>fp, "<p><a href='recipes.html'>Recipes</a>"
print >>fp, "<p><a href='inventory.html'>Inventory</a>"

print >>fp, """<h3>Available Liquor Types</h3>"""

print >>fp, "<ul>"
for (mfg, lqr, typ) in drinkz.db._bottle_types_db:
    print >>fp, "<li>"
    print >>fp, mfg, "&#151;", lqr, "&#151;", typ
print >>fp, "</ul>"
fp.close()


generate_index()
