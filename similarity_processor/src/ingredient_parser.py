import os
import sys
import json
sys.path.append(os.path.join(os.path.dirname(__file__), ""))
import food_item_matcher as matcher
import database_interface as db


if __name__ == "__main__":
    dbInterface = db.DatabaseInterface()
    recipes = dbInterface.recipes
    match = matcher.FoodItemMatcher()
    recipe_dict = {}

    # Match all the ingredients in each recipe to a known food ingredient.
    for i, recipe in enumerate(recipes):
        print(recipe['title'])
        phrase = ""
        for ingredient in recipe['ingredients']:
            phrase += ", " + ingredient
        phrase = phrase[1:].strip()
        matches = match.match_food_item(phrase)
        print("{}: {} => {}".format(i, recipe['title'], matches))
        r = {
            '_id': str(recipe['_id']),
            'title': recipe['title'],
            'ingredients': matches
        }
        recipe_dict[str(recipe['_id'])] = r

    # Write out the json file for the parsed ingredients
    with open('../resources/parsed_ingredients.json', 'w') as f:
        json.dump(recipe_dict, f)
