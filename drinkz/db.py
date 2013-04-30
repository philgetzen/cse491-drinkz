"""
Database functionality for drinkz information.

Recipes are stored in a set because it allows us to have a name and a list of tuples per recipe.
"""

import recipes, convert, sqlite3, sql_clear_db

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()

#  temporary storage for results of a form to display in jinja template, clear before use
_tmp_results = []

# Our SQLite database
# db = sqlite3.connect('drinkz.db')
# c = db.cursor()

# c.execute('SELECT * FROM drink_types')
# print c.fetchall()


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()
    _tmp_results = []

    sql_clear_db.clear()
    # sql_pull_db()


def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes_db)
    dump(tosave, fp)

    fp.close()


def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes_db) = loaded

    fp.close()


# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass


class DuplicateRecipeName(Exception):
    pass


def sql_pull_db():
    sql_pull_liquor_types()
    sql_pull_inventory()
    sql_pull_recipes()


def sql_pull_liquor_types():
    db = sqlite3.connect('drinkz.db')
    c = db.cursor()

    c.execute('SELECT * FROM drink_types')
    liquor_types = c.fetchall()

    _bottle_types_db.clear()

    for bt_id, mfg, liquor, typ in liquor_types:
        _bottle_types_db.add((mfg, liquor, typ))

    db.close()


def sql_add_liquor_type(mfg, liquor, typ):
    db = sqlite3.connect('drinkz.db')
    c = db.cursor()

    c.execute('INSERT INTO drink_types (mfg, liquor, typ) VALUES (?, ?, ?)', (mfg, liquor, typ))

    db.commit()
    db.close()

    sql_pull_db()


def sql_pull_inventory():
    db = sqlite3.connect('drinkz.db')
    c = db.cursor()

    c.execute('''SELECT drink_types.mfg, drink_types.liquor, inventory.amount
                FROM inventory, drink_types
                WHERE inventory.drink_type_id = drink_types.id''')
    inventory = c.fetchall()

    _inventory_db.clear()

    for mfg, liquor, amount in inventory:
        _inventory_db[(mfg, liquor)] = amount

    db.close()


def sql_insert_inventory(mfg, liquor, amount):
    sql_change_inventory('insert', mfg, liquor, amount)


def sql_update_inventory(mfg, liquor, amount):
    sql_change_inventory('update', mfg, liquor, amount)


def sql_change_inventory(sql, mfg, liquor, amount):
    db = sqlite3.connect('drinkz.db')
    c = db.cursor()

    print mfg, liquor

    c.execute('''SELECT id
                        FROM drink_types
                        WHERE drink_types.mfg = ? AND drink_types.liquor = ?''', (mfg, liquor))
    result = c.fetchall()

    if(sql == 'update'):
        for bt_id in result[0]:
            # print "BTID: ", bt_id
            c.execute('''UPDATE inventory
                            SET amount = ?
                            WHERE drink_type_id = ?''', (amount, bt_id))

        # print "RESULT: ", result[0]

    elif(sql == 'insert'):
        for bt_id in result[0]:
            c.execute('INSERT INTO inventory (drink_type_id, amount) VALUES (?, ?)', (bt_id, amount))

    db.commit()
    db.close()

    sql_pull_db()


def sql_pull_recipes():
    db = sqlite3.connect('drinkz.db')
    c = db.cursor()

    c.execute('''SELECT r.id, r.recipe_name, i.ingredient, i.amount
                FROM recipes AS r, ingredients AS i, recipe_join AS rj
                WHERE rj.recipe_id = r.id AND rj.ingredient_id = i.id''')
    recipe_results = c.fetchall()

    _recipes_db.clear()

    n = ""
    ing_list = []

    prev_id = 1

    for r_id, name, ingredient, amount in recipe_results:
        if(prev_id != r_id):
            r = recipes.Recipe(n, ing_list)
            _recipes_db.add(r)

            n = name
            ing_list = []
            ing_list.append((ingredient.encode("utf8"), amount.encode("utf8")))
        else:
            n = name
            ing_list.append((ingredient.encode("utf8"), amount.encode("utf8")))

        prev_id = r_id

    r = recipes.Recipe(n, ing_list)
    _recipes_db.add(r)

    db.close()


def sql_add_recipe(r):
    db = sqlite3.connect('drinkz.db')
    c = db.cursor()

    c.execute('INSERT INTO recipes (recipe_name) VALUES (?)', (r.name,))
    c.execute('SELECT id FROM recipes WHERE recipe_name = ?', (r.name,))
    recipe_result = c.fetchall()

    r_id = 0
    for i in recipe_result[0]:
        r_id = int(i)

    for ing, amt in r.needIngredients:
        c.execute('INSERT INTO ingredients (ingredient, amount) VALUES (?, ?)', (ing, amt))
        c.execute('SELECT id FROM ingredients WHERE ingredient = ? AND amount = ?', (ing, amt))
        ing_result = c.fetchall()

        i_id = 0
        for a in ing_result[0]:
            i_id = int(a)

        c.execute('INSERT INTO recipe_join (recipe_id, ingredient_id) VALUES (?, ?)', (r_id, i_id))

    db.commit()
    db.close()

    sql_pull_db()


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    # _bottle_types_db.add((mfg, liquor, typ))
    sql_add_liquor_type(mfg, liquor, typ)


def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False


def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    sql_pull_db()

    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    amountTotal = convert.convert_to_ml(amount)

    # sql_add_inventory(mfg, liquor, amount+" ml")

    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] += amountTotal
        sql_update_inventory(mfg, liquor, _inventory_db[(mfg, liquor)])
    else:
        # _inventory_db[(mfg, liquor)] = amountTotal
        sql_insert_inventory(mfg, liquor, amountTotal)

    sql_pull_db()


def check_inventory(mfg, liquor):
    if (mfg, liquor) in _inventory_db:
        return True
    return False


def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    if (mfg, liquor) in _inventory_db:
        return _inventory_db[(mfg, liquor)]


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (mfg, liquor) in _inventory_db:
        yield mfg, liquor


def add_recipe(r):
    # sql_pull_db()

    for rec in _recipes_db:
        if rec.name == r.name:
            err = "Duplicate Recipe:  %s", r.name
            raise DuplicateRecipeName(err)
    # _recipes_db.add(r)
    sql_add_recipe(r)

    sql_pull_db()


def get_recipe(name):
    for r in _recipes_db:
        if r.name == name:
            return r


def get_all_recipes_by_name():
    recipesSet = set()
    for r in _recipes_db:
        recipesSet.add(r.name)
    return recipesSet


def get_all_recipes():
    recipesSet = set()
    for r in _recipes_db:
        recipesSet.add(r)
    return recipesSet


def check_inventory_for_type(typ):
    for (m, l) in _inventory_db:
        if (m, l, typ) in _bottle_types_db:
            yield (m, l)


def get_liquor_type_amount(typ):
    amountTotal = 0
    for (m, l) in _inventory_db:
        if (m, l, typ) in _bottle_types_db:
            amountTotal += _inventory_db[(m, l)]
    return amountTotal


def available_recipes():
    recipeSet = set()
    add = True
    for recipe in _recipes_db:
        add = True
        for (typ, amount) in recipe.needIngredients:
            liquors = check_inventory_for_type(typ)
            # If we don't have that type in our inventory we can't make the recipe
            if not liquors:
                add = False
                break
            if get_liquor_type_amount(typ) < convert.convert_to_ml(amount):
                add = False
                break
        if add:
            recipeSet.add(recipe)
    return recipeSet
