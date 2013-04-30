import sqlite3, os


def clear():
    try:
        os.unlink('drinkz.db')  # start fresh
    except OSError:
        pass

    db = sqlite3.connect('drinkz.db')

    c = db.cursor()

    # Create our drink type table
    c.execute('CREATE TABLE drink_types (id INTEGER PRIMARY KEY ASC, mfg TEXT, liquor TEXT, typ TEXT)')

    # Create our inventory table
    c.execute('CREATE TABLE inventory (id INTEGER PRIMARY KEY ASC, drink_type_id INTEGER REFERENCES drink_types, amount INTEGER)')

    c.execute('CREATE TABLE recipes (id INTEGER PRIMARY KEY ASC, recipe_name TEXT)')
    c.execute('CREATE TABLE ingredients (id INTEGER PRIMARY KEY ASC, ingredient TEXT, amount TEXT)')
    c.execute('''CREATE TABLE recipe_join (id INTEGER PRIMARY KEY ASC, recipe_id INTEGER REFERENCES recipes,
                    ingredient_id INTEGER REFERENCES ingredients)''')

    db.commit()
    db.close()
