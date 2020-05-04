from pymongo import MongoClient
from fuzzywuzzy import fuzz
import ssl


class AllergenProcessor:
    def __init__(self):
        # Create a connection to the Mongo Database (Note: Needed to disable SSL Certs for my local machine)
        client = MongoClient("mongodb+srv://"
                             "AltAllergenDBAdmin:allergenadmin@altallergendbcluster-kkirt.mongodb.net/altAllergen"
                             "?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)

        # Connect to the altAllergen database
        self.db = client.altAllergen

        # Retrieve the lists of known allergen ingredients from the allergens collection
        self.allergens = self.get_allergens()

        self.fuzz_threshold = 60

    def get_allergens(self):
        allergens = []
        for allergen in self.db.allergens.find():
            allergens.append({
                'name': allergen['group'],
                'ingredients': allergen['ingredients']
            })

        return allergens

    def process_recipes(self):

        self.get_recipe_counts()

        # Process all recipe ingredients in the recipes collection
        for recipe in self.db.recipes.find({"allergens": {"$exists": False}}, no_cursor_timeout=True):
            ingredient_text = ' '.join(recipe['ingredients'])
            recipe_allergens = []

            # Look at all possible allergen groups
            for allergen_group in self.allergens:
                recipe_allergen_ingredients = []

                # Look at all possible allergen ingredients within an allergen group
                for allergen_ingredient in allergen_group['ingredients']:

                    # Calculate the likelihood that the allergen ingredient is in
                    # the recipe's ingredient list or the recipe's instructions
                    ingredient_list_likelihood = fuzz.token_set_ratio(ingredient_text, allergen_ingredient)
                    instructions_likelihood = fuzz.token_set_ratio(recipe['instructions'], allergen_ingredient)

                    if ingredient_list_likelihood > self.fuzz_threshold or instructions_likelihood > self.fuzz_threshold:
                        recipe_allergen_ingredients.append(allergen_ingredient)

                # If any allergen group ingredients were found, then the recipe
                # will be flagged for the particular allergen group
                if len(recipe_allergen_ingredients) > 0:
                    recipe_allergens.append({
                        'group': allergen_group['name'],
                        'ingredients': recipe_allergen_ingredients
                    })

            # Add flags to the recipe for any potential allergen ingredients
            if len(recipe_allergens) > 0:
                recipe['allergens'] = recipe_allergens
                self.db.recipes.save(recipe)

    def get_recipe_counts(self):
        print("Total Recipes:", self.db.recipes.count_documents({}))
        print("Allergen Containing Recipes:", self.db.recipes.count_documents({"allergens": {"$exists": True}}))
        print("Allergen Free Recipes:", self.db.recipes.count_documents({"allergens": {"$exists": False}}))


if __name__ == "__main__":
    processor = AllergenProcessor()
    processor.get_recipe_counts()
    processor.process_recipes()
    processor.get_recipe_counts()
