"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db = []
_inventory_db = {}


def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = []
    _inventory_db = {}


# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.append((mfg, liquor, typ))


def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False


def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    amounts = []
    amounts = amount.split(" ")
    amountTotal = 0

    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)

    if amounts[1].lower() == "oz":
        amountTotal += int(int(amounts[0]) * 29.5735)
    elif amounts[1].lower() == "ml":
        amountTotal += int(amounts[0])

    if (mfg, liquor) in _inventory_db:
        _inventory_db[(mfg, liquor)] += amountTotal
    else:
        _inventory_db[(mfg, liquor)] = amountTotal

    # just add it to the inventory database as a tuple, for now.
    # _inventory_db.append((mfg, liquor, amount))


def check_inventory(mfg, liquor):
    if (mfg, liquor) in _inventory_db:
        return True
    return False


def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    # amounts = []
    # result = 0
    # for (m, l, amount) in _inventory_db:
    #     if mfg == m and liquor == l:
    #         #Split the amounts into values and labels
    #         amounts = amount.split(" ")
    #         #If the label equals ounces
    #         if amounts[1] == "oz" or amounts[1] == "Oz" or amounts[1] == "OZ" or amounts[1] == "oZ":
    #             #Add the amount * the conversion rate
    #             result += int(amounts[0]) * 29.5735
    #         elif amounts[1] == "ml" or amounts[1] == "Ml" or amounts[1] == "ML" or amounts[1] == "mL":
    #             #Just return the amount given
    #             result += int(amounts[0])
    if (mfg, liquor) in _inventory_db:
        return str(_inventory_db[(mfg, liquor)]) + " ml"
    #Return a string of the result
    # return str(int(result)) + " ml"


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (mfg, liquor) in _inventory_db:
        yield mfg, liquor
