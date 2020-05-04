from pymongo import MongoClient
import ssl


class DatabaseInterface:
    def __init__(self):
        # Create the connection
        client = MongoClient("mongodb+srv://"
                             "AltAllergenDBAdmin:allergenadmin@altallergendbcluster-kkirt.mongodb.net/altAllergen"
                             "?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
        self.db = client.altAllergen

        #self.recipes = self.get_recipes()

        self.allergens = self.get_allergens()

    def get_recipes(self):
        recipes = []
        for recipe in self.db.recipes.find():
            r = {
                '_id': recipe['_id'],
                'title': recipe['title'],
                'ingredients': recipe['ingredients'],
                'instructions': recipe['instructions'],
            }
            recipes.append(r)
        return recipes

    def get_allergens(self):
        allergens = []
        for allergen in self.db.allergens.find():
            allergens.append({
                'name': allergen['group'],
                'ingredients': allergen['ingredients']
            })
        return allergens

    def print_recipes(self):
        for recipe in self.recipes:
            print(recipe)

    def print_allergens(self):
        for allergen in self.allergens:
            print(allergen['name'])
            for ingredient in allergen['ingredients']:
                print("\t" + ingredient)


if __name__ == "__main__":
    dbInterface = DatabaseInterface()
    dbInterface.print_allergens()
