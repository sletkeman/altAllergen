import json
import os
import sys
import numpy as np
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

        self.ingredients_to_index_map = {}
        self.index_to_ingredient_map = {}
        self.recipe_to_index_map = {}
        self.index_to_recipe_map = {}
        self.allergens_maps = {}
        self.recipe_ingredients_indexes = {}
        self.similar_recipes = {}

        current_ingredient_index = 0
        for i, recipe in enumerate(self.recipes.items()):
            # Add recipes to their respective indexes
            if recipe[0] not in self.recipe_to_index_map:
                self.recipe_to_index_map[recipe[0]] = i
                self.index_to_recipe_map[i] = recipe[0]
            # Go through each ingredient in the recipe and add it to the ingredient index map
            # Also add all of the ingredient indexes to the recipe ingredient indexes map
            indexes = []
            for ingredient in recipe[1]['ingredients']:
                if ingredient not in self.ingredients_to_index_map:
                    self.ingredients_to_index_map[ingredient] = current_ingredient_index
                    self.index_to_ingredient_map[current_ingredient_index] = ingredient
                    indexes.append(current_ingredient_index)
                    current_ingredient_index = current_ingredient_index + 1
                else:
                    indexes.append(self.ingredients_to_index_map[ingredient])
            self.recipe_ingredients_indexes[recipe[0]] = indexes

        # Build allergen indices
        for allergen in self.allergens:
            indexes = []
            for ingredient in allergen['ingredients']:
                if ingredient not in self.ingredients_to_index_map:
                    self.ingredients_to_index_map[ingredient] = current_ingredient_index
                    self.index_to_ingredient_map[current_ingredient_index] = ingredient
                    indexes.append(current_ingredient_index)
                    current_ingredient_index = current_ingredient_index + 1
                else:
                    indexes.append(self.ingredients_to_index_map[ingredient])
            self.allergens_maps[allergen['name']] = indexes
        self.allergens_maps["all"] = []



        # Build recipe to ingredient matrix
        self.recipe_to_ingredient_matrix = np.zeros((len(self.recipe_to_index_map), len(self.ingredients_to_index_map)),
                                                    dtype=int)
        for i, recipe in enumerate(self.recipe_to_index_map):
            r_index = self.recipe_to_index_map[recipe]
            for j, ingredient in enumerate(self.recipe_ingredients_indexes[recipe]):
                i_index = ingredient
                self.recipe_to_ingredient_matrix[r_index, i_index] = 1

        # print(self.recipe_to_ingredient_matrix[10, :])

        # print(self.recipes[self.index_to_recipe_map[10]]['title'])
        # print(self.recipes[self.index_to_recipe_map[10]]['ingredients'])

    def calculate_similarites(self):
        for i, recipe in enumerate(self.recipe_to_index_map):
            if i > 10:
                break
            self.similar_recipes[recipe] = self.recipes[recipe]
            print("{}: Processing {}, ID: {}.".format(i, self.recipes[recipe]['title'], recipe))
            r_index = self.recipe_to_index_map[recipe]
            r = self.recipe_to_ingredient_matrix[r_index, :]
            r = r.reshape((1, r.shape[0]))
            sims = self.recipe_to_ingredient_matrix[r_index, :] @ self.recipe_to_ingredient_matrix.T
            sims = sims / len(self.recipe_ingredients_indexes[recipe])
            sorted_args = np.argsort(-1 * sims)
            for allergen in self.allergens_maps.items():
                print("\nTop 10 similar recipes for {} with no {}.".format(self.recipes[recipe]['title'], allergen[0]))
                count = 0
                top_ten = {}
                for i, sim in enumerate(sorted_args):
                    if sim == r_index:
                        continue
                    ingredients_list = self.recipe_to_ingredient_matrix[sim, :]
                    sum_shared = np.sum(ingredients_list[allergen[1]])
                    if sum_shared == 0:
                        id = self.recipes[self.index_to_recipe_map[sim]]['title']
                        print("{} Title: {}, ID: {}, Sim: {}".format(count+1,
                                                                     id, self.index_to_recipe_map[sim], sims[sim]))
                        count = count + 1
                        top_ten[self.index_to_recipe_map[sim]] = sims[sim]
                    if count >= 10:
                        if allergen[0] == "all":
                            key = "top_ten_{}".format(allergen[0])
                        else:
                            key = "top_ten_no_{}".format(allergen[0])
                        self.similar_recipes[recipe][key] = top_ten
                        break
        with open('../resources/ingredient_similarities.json', 'w') as f:
            json.dump(self.similar_recipes, f)


if __name__ == "__main__":
    ism = IngredientSimilarityMeasurer()
    start = datetime.now()
    ism.calculate_similarites()
    print("Execution time: " + str(datetime.now() - start))
