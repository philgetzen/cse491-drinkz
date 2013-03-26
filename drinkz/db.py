"""
Database functionality for drinkz information.

Recipes are stored in a set because it allows us to have a name and a list of tuples per recipe.
"""

from . import recipes, convert

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipes_db = set()


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = set()


def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass


class DuplicateRecipeName(Exception):
    pass


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))


def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False


def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."

    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    amountTotal = convert.convert_to_ml(amount)

    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] += amountTotal
    else:
        _inventory_db[(mfg, liquor)] = amountTotal


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
    for rec in _recipes_db:
        if rec.name == r.name:
            err = "Duplicate Recipe:  %s", r.name
            raise DuplicateRecipeName(err)
    _recipes_db.add(r)


def get_recipe(name):
    for r in _recipes_db:
        if r.name == name:
            return r


def get_all_recipes():
    recipesSet = set()
    for r in _recipes_db:
        recipesSet.add(r)
    return recipesSet


def check_inventory_for_type(typ):
    for (m, l) in _inventory_db:
        if (m, l, typ) in _bottle_types_db:
            yield (m, l)
