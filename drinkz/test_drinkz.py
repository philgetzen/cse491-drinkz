"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/')  # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data


def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'


def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'

    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')


def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')


def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass


def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount


def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n


def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount


# Phil Getzen's Test Liquor Amount 3
# The answer is usually zero at the end of the night.
def test_get_liquor_amount_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '25 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1739.3375, amount


# Phil Getzen's Test Liquor Amount 4
# The answer is usually zero at the end of the night.
def test_get_liquor_amount_4():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '2 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '0 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 2.0, amount


# Phil Getzen's Test Liquor Amount 5
# The answer is usually zero at the end of the night.
def test_get_liquor_amount_5():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '0 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '100 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 2957.35, amount


# Phil Getzen's Test Liquor Amount 6
# The answer is usually zero at the end of the night.
def test_get_liquor_amount_6():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '16 oz')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '32 oz')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1419.528, amount


def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n


def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code


def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    db.add_bottle_type('A', 'B', 'C')
    db.add_to_inventory('A', 'B', '100 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label'), ('A', 'B')], x


# Phil Getzen's Test Load Bottle Types 1
def test_load_bottle_types_1():
    db._reset_db()

    data = "#This line is for a comment test"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n


# Phil Getzen's Test Load Bottle Types 2
def test_load_bottle_types_2():
    db._reset_db()

    data = ""
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert n == 0, n


#Phil Getzen's Script Load Inventory Test
def test_script_load_inventory_1():
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('li', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt', 'test-data/inventory-data-2.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code


def test_check_inventory_for_type():
    db._reset_db

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    db.add_bottle_type('A', 'B', 'C')
    db.add_to_inventory('A', 'B', '100 ml')

    x = []
    for mfg, liquor in db.check_inventory_for_type('blended scotch'):
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x