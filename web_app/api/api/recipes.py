"""
    basic ReST actions.
"""

from bson.objectid import ObjectId
import re
from json import loads
from flask import abort
from bson.json_util import dumps
from services.mongo import get_collection


def get_recipe(recipe_id):
    try:
        o_id = ObjectId(recipe_id)
        recipies = get_collection('recipes')
        recipe = recipies.find_one({"_id": o_id})
        return loads(dumps(recipe))
    except RuntimeError as ex:
        abort(500, ex.args[1])

def get_recipes(title=None, allergen=None):
    try:
        recipies = get_collection('recipes')

        query = {}
        result = {
            'stats': {},
            'recipes': []
        }

        if title:
            regx = re.compile(title, re.IGNORECASE)
            query['title'] = regx
            result['stats']['title'] = recipies.find(query).count()
        if allergen and allergen[0] != '':
            query['allergens'] = {"$not": {"$elemMatch": { "$or": [{"group":a} for a in allergen] }}}
            result['stats']['allergen'] = recipies.find(query).count()

        # Find the counts of individual allergen ingredients that may be in a recipe of a given title
        if title and allergen and allergen[0] != '':
            query_cursor = recipies.aggregate([
                {"$match": {"title": regx}},
                {"$unwind": "$allergens"},
                {"$match": {"allergens.group": allergen[0]}},
                {"$unwind": "$allergens.ingredients"},
                {"$group": {
                    "_id": {"ingredient": "$allergens.ingredients"},
                    "total": {"$sum": 1}
                }},
                {"$project": {
                    "_id": 0,
                    "ingredient": "$_id.ingredient",
                    "count": "$total"
                }}
            ])

            allergen_ingredients = []
            for row in query_cursor:
                allergen_ingredients.append(row)

            # Sort the results in descending order
            allergen_ingredients.sort(key=lambda x: x['count'], reverse=True)
            result['stats']['allergen_ingredients'] = allergen_ingredients

        for (i, recipe) in enumerate(recipies.find(query)):
            result['recipes'].append(loads(dumps(recipe)))
            if i >= 199:
                break
        return result
    except RuntimeError as ex:
        abort(500, ex.args[1])
