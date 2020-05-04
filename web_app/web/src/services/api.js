import axios from "axios";
import qs from "query-string";

axios.defaults.baseURL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8080/api/"
    : "/api/";

const fetchAllergens = async () => {
  const { data } = await axios.get(`/allergens`);
  return data;
};

const fetchRecipes = async (title, allergen) => {
  const query = qs.stringify({ title, allergen });
  const { data } = await axios.get(`/recipes?${query}`);
  return data;
};

const fetchRecipe = async recipeId => {
  const { data } = await axios.get(`/recipe/${recipeId}`);
  return data;
};

const fetchLinks = async (recipeId, allergens, number) => {
  const query = qs.stringify({ number, allergens });
  const { data } = await axios.get(`/similar/${recipeId}?${query}`);
  return data;
};

export { fetchAllergens, fetchRecipes, fetchRecipe, fetchLinks };
