"""
    basic ReST actions.
"""

from json import loads
from bson.json_util import dumps
from flask import abort
from services.mongo import get_collection

def get_allergens():
    try:
        result = []
        allergens = get_collection('allergens')
        for allergen in allergens.find():
            result.append(loads(dumps(allergen)))
        return result
    except RuntimeError as ex:
        abort(500, ex.args[1])
