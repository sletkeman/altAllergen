import spacy
import re
from fuzzywuzzy import fuzz

FUZZY_RATIO = 80
MEASUREMENT_RATIO = 90
MEASUREMENTS = ["cups", "teaspoons", "tablespoons", "pounds", "lbs", "packages", "ounces", "ozs", "gallons",
                "containers", "cup", "teaspoon", "tablespoon", "pound", "lb", "package", "ounce", "oz", "gallon",
                "container"]


class FoodItemMatcher:

    def __init__(self):
        self.food_dictionary = self.load_food_dictionary("../resources/foodb_2017_06_29_csv/foods.csv")
        self.nlp = spacy.load("en_core_web_sm")

    def match_food_item(self, food_string):
        doc = self.nlp(food_string.lower())
        food_items = []
        food_word = ""
        for chunk in doc.noun_chunks:
            any_match = False
            new_text = chunk.text
            pattern = '[0-9]|\/|\(|\)|\.'
            new_text = re.sub(pattern,'',new_text)
            for item in MEASUREMENTS:
                if new_text.find(item) >= 0:
                    new_text = new_text.replace(item, "")
            new_text = new_text.strip()
            #print(new_text)
            best_ratio = 0
            for entry in self.food_dictionary:
                ratio = fuzz.ratio(new_text.lower(), entry.lower())
                if ratio > FUZZY_RATIO and ratio > best_ratio:
                    any_match = True
                    food_word = entry.lower()
                    best_ratio = ratio
            best_ratio = 0
            if not any_match:
                for word in new_text.split(" "):
                    for entry in self.food_dictionary:
                        ratio = fuzz.ratio(word.lower(), entry.lower())
                        if ratio > FUZZY_RATIO and ratio > best_ratio:
                            any_match = True
                            food_word = entry.lower()
                            best_ratio = ratio
            if any_match:
                if food_word not in food_items:
                    food_items.append(food_word)
        return food_items

    def load_food_dictionary(self, filename):
        food_dict = set()
        is_first_line = True
        with open(filename, encoding="ISO-8859-1") as file:
            for line in file:
                # Skip the header line
                if is_first_line:
                    is_first_line = False
                else:
                    foods = line.split(",")
                    if len(foods) >= 2:
                        if foods[0].isdigit():
                            food_cleaned = foods[1].lower().replace("\"", "")
                            food_cleaned = re.sub("[\(\[].*?[\)\]]", "", food_cleaned)
                            food_cleaned_words = food_cleaned.split(" ")
                            to_add = ""
                            for word in food_cleaned_words:
                                if len(word) > 0:
                                    if word[0] == "(" or word[-1] == ")":
                                        pass
                                    else:
                                        to_add += " " + word
                            food_dict.add(to_add.strip())
        return food_dict


if __name__ == "__main__":
    foodMatcher = FoodItemMatcher()
    items = foodMatcher.match_food_item("6 pork chops, 1 teaspoon garlic powder, 1 teaspoon seasoning salt, 2 egg, beaten, 1/4 cup all-purpose flour, 2 cups Italian-style seasoned bread crumbs, 4 tablespoons olive oil, 1 (10.75 ounce) can condensed cream of mushroom soup, 1/2 cup milk, 1/3 cup white wine")
    for item in items:
        print(item)
