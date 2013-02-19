# from . import db


class Recipe:
    def __init__(self, name, ing):
        self.name = name
        self.needIngredients = ing

    def need_ingredients(self):
        return self.needIngredients
