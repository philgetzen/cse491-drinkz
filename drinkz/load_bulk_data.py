"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package


def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = csv_reader(fp)

    x = []
    n = 0
    for line in reader:
        try:
            (mfg, name, typ) = line
        except:
            print "Improper Line Format"
            continue
        try:
            db.add_bottle_type(mfg, name, typ)
        except:
            print "Bottle Type Could Not Be Added"
            continue
        n += 1
    return n


def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to databaseself.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = csv_reader(fp)

    x = []
    n = 0
    for line in reader:
        try:
            (mfg, name, amount) = line
        except:
            print "Improper Line Format"
            continue
        try:
            db.add_to_inventory(mfg, name, amount)
        except:
            print "Inventory Could Not Be Loaded"
            continue
        n += 1
    return n


def csv_reader(fp):

    reader = csv.reader(fp)

    for line in reader:
        if len(line) > 0:
            if line[0].startswith('#'):
                continue
            if not line[0].strip():
                continue
        else:
            continue
        yield line
