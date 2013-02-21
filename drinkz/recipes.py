import db


class Recipe:

    def __init__(self, name, ing):
        self.name = name
        self.needIngredients = ing

    def need_ingredients(self):
        amountInv = 0
        amountNeeded = 0

        listOfKeys = []
        listOfTypes = []
        listOfAmounts = []
        listOfNeeded = []

        # get list of keys for the types in inventory
        for (typ, amount) in self.needIngredients:
            for mfg, liquor in db.check_inventory_for_type(typ):
                listOfKeys.append((mfg, liquor))
            listOfTypes.append((typ, listOfKeys))
            listOfKeys = []

        for (t, lk) in listOfTypes:
            amountInv = 0
            for (m, l) in lk:
                if (m, l) in db._inventory_db or listOfTypes[1] == []:
                    if db._inventory_db[(m, l)] > amountInv:
                        amountInv = db._inventory_db[(m, l)]
            listOfAmounts.append((t, amountInv))

        for (t, a) in self.needIngredients:
            for (typ, amount) in listOfAmounts:
                if t == typ:
                    amountNeeded = float(db.convert_to_ml(a)) - float(amount)
                    if amountNeeded > 0:
                        listOfNeeded.append((typ, amountNeeded))
        return listOfNeeded
