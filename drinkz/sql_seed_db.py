import sqlite3, os

try:
    os.unlink('drinkz.db')  # start fresh
except OSError:
    pass

db = sqlite3.connect('drinkz.db')

c = db.cursor()

# Create our drink type table
c.execute('CREATE TABLE drink_types (id INTEGER PRIMARY KEY ASC, mfg TEXT, liquor TEXT, typ TEXT)')

# Insert our seeded drink types
c.execute('INSERT INTO drink_types (mfg, liquor, typ) VALUES (?, ?, ?)', ('Johnnie Walker', 'black label', 'blended scotch'))
c.execute('INSERT INTO drink_types (mfg, liquor, typ) VALUES (?, ?, ?)', ('Uncle Herman\'s', 'moonshine', 'blended scotch'))
c.execute('INSERT INTO drink_types (mfg, liquor, typ) VALUES (?, ?, ?)', ('Gray Goose', 'vodka', 'unflavored vodka'))
c.execute('INSERT INTO drink_types (mfg, liquor, typ) VALUES (?, ?, ?)', ('Rossi', 'extra dry vermouth', 'vermouth'))

c.execute('SELECT * FROM drink_types')
print "\nBottle Types Added: ", c.fetchall(), "\n"

# Create our inventory table
c.execute('CREATE TABLE inventory (id INTEGER PRIMARY KEY ASC, drink_type_id INTEGER REFERENCES drink_types, amount INTEGER)')

# Insert our seeded inventory amounts
c.execute('INSERT INTO inventory (drink_type_id, amount) VALUES (?, ?)', (1, 500))
c.execute('INSERT INTO inventory (drink_type_id, amount) VALUES (?, ?)', (2, 100))
c.execute('INSERT INTO inventory (drink_type_id, amount) VALUES (?, ?)', (3, 20.5))
c.execute('INSERT INTO inventory (drink_type_id, amount) VALUES (?, ?)', (4, 10.3))

c.execute('''SELECT drink_types.mfg, drink_types.liquor, inventory.amount
                FROM inventory, drink_types
                WHERE inventory.drink_type_id = drink_types.id''')

print "\nInventory Amounts Added: ", c.fetchall(), "\n"

c.execute('CREATE TABLE recipes (id INTEGER PRIMARY KEY ASC, recipe_name TEXT)')
c.execute('CREATE TABLE ingredients (id INTEGER PRIMARY KEY ASC, ingredient TEXT, amount TEXT)')
c.execute('''CREATE TABLE recipe_join (id INTEGER PRIMARY KEY ASC, recipe_id INTEGER REFERENCES recipes,
ingredient_id INTEGER REFERENCES ingredients)''')

c.execute('INSERT INTO recipes (recipe_name) VALUES (?)', ('scotch on the rocks',))
c.execute('INSERT INTO ingredients (ingredient, amount) VALUES (?, ?)', ('blended scotch', '10 oz'))
c.execute('INSERT INTO recipe_join (recipe_id, ingredient_id) VALUES (?, ?)', (1, 1))

c.execute('INSERT INTO ingredients (ingredient, amount) VALUES (?, ?)', ('scotch', '20 oz'))
c.execute('INSERT INTO recipe_join (recipe_id, ingredient_id) VALUES (?, ?)', (1, 2))

c.execute('INSERT INTO recipes (recipe_name) VALUES (?)', ('bloody mary',))
c.execute('INSERT INTO ingredients (ingredient, amount) VALUES (?, ?)', ('whiskey', '80 oz'))
c.execute('INSERT INTO recipe_join (recipe_id, ingredient_id) VALUES (?, ?)', (2, 3))

c.execute('INSERT INTO recipes (recipe_name) VALUES (?)', ('I don\'t care',))
c.execute('INSERT INTO ingredients (ingredient, amount) VALUES (?, ?)', ('blended scotch', '5 oz'))
c.execute('INSERT INTO recipe_join (recipe_id, ingredient_id) VALUES (?, ?)', (3, 4))


c.execute('''SELECT r.id, r.recipe_name, i.ingredient, i.amount
                FROM recipes AS r, ingredients AS i, recipe_join AS rj
                WHERE rj.recipe_id = r.id AND rj.ingredient_id = i.id''')

print "\nRecipes Added: ", c.fetchall(), "\n"


# Commit our seeded data and close the connection
print "*Finished seeding database*"
db.commit()
db.close()
