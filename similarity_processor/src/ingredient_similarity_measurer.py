import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ""))
import database_interface as db
from datetime import datetime


class IngredientSimilarityMeasurer:

    def __init__(self):
        self.recipes = {}
        with open("../resources/parsed_ingredients.json") as f:
            self.recipes = json.load(f)

        database = db.DatabaseInterface()
        database.get_allergens()
        self.allergens = database.allergens
        self.similar_recipes = {}

    def calculate_similarites(self):
        for i, recipe in enumerate(self.recipes.items()):
            if i > 10:
                break
            self.similar_recipes[recipe[0]] = recipe[1]
            print("\n\n{}: Processing {}, ID: {}.".format(i, recipe[1]['title'], recipe[0]))
            # Compare each recipe's ingredients to every other recipe's ingredients.
            recipe_sims = {}
            for node in self.recipes.items():
                if node[1]['_id'] == recipe[1]['_id']:
                    continue
                # Count up each shared ingredient and divide it by the total number of ingredients to get the
                # similarity measure
                count = 0
                for ingredient in recipe[1]['ingredients']:
                    if ingredient in node[1]['ingredients']:
                        count = count + 1
                similarity_measure = count / float(len(recipe[1]['ingredients']))
                #print("Similarity measure against {}: {}".format(node[1]['title'], similarity_measure))
                recipe_sims[node[1]['_id']] = similarity_measure
            recipe_sims = {k: v for k, v in sorted(recipe_sims.items(), key=lambda item: item[1], reverse=True)}
            for allergen in self.allergens:
                print("\nTop 10 similar recipes for {} with no {}.".format(recipe[1]['title'], allergen['name']))
                count = 0
                top_ten = []
                for i, r in enumerate(recipe_sims.items()):
                    r_set = set(self.recipes[r[0]]['ingredients'])
                    allergen_set = set(allergen['ingredients'])
                    if len(r_set.intersection(allergen_set)) == 0:
                        print("Title: {}, ID: {}, Sim: {}".format(self.recipes[r[0]]['title'], r[0], r[1]))
                        count = count + 1
                        top_ten.append(r[0])
                    if count >= 10:
                        key = "top_ten_no_{}".format(allergen['name'])
                        self.similar_recipes[recipe[0]][key] = top_ten
                        break
        with open('../resources/ingredient_similarities.json', 'w') as f:
            json.dump(self.similar_recipes, f)


if __name__ == "__main__":
    ism = IngredientSimilarityMeasurer()
    start = datetime.now()
    ism.calculate_similarites()
    print("Execution time: " + str(datetime.now() - start))
