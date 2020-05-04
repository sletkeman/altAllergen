"""
    basic ReST actions.
"""

from flask import abort
from services.ingredient_similarity_measure_dot import IngredientSimilarityMeasurer

ism = IngredientSimilarityMeasurer()


def get_links_nodes(recipies):
    links = []
    nodes = {}
    for r in recipies:
        nodes[r["recipe"]] = {
            "type": "recipe",
            "score": r["sim"],
            "recipe_id": r["recipe_id"],
            "name": r["recipe"]
        }
        for i in r['ingredients']:
            links.append({
                'source': r['recipe'],
                'target': i
            })
            if i not in nodes:
                nodes[i] = {
                    "type": "ingredient",
                    "name": i
                }
    return (links, nodes)

def get_similar(recipe_id, allergens=[], number=10):
    try:
        # 5e716fabef66fb965f4161b9
        result = ism.calculate_similarites(recipe_id, allergens, number)
        (links, nodes) = get_links_nodes(result)
        return {
            "links": links,
            "nodes": nodes
        }
    except RuntimeError as ex:
        abort(500, ex.args[1])
