import { GET_RECIPES, GET_ALLERGENS, GET_RECIPE } from "../actions";
import {
  SET_RECIPES,
  SET_ALLERGENS,
  SET_SEARCH_PARAMS,
  SET_ERROR,
  SET_RECIPE
} from "../mutations";

import { fetchRecipes, fetchAllergens, fetchRecipe } from "../../services/api";

const state = {
  recipes: [],
  recipe: {},
  stats: {},
  allergens: [],
  searchParams: {
    title: "",
    allergens: []
  }
};

const actions = {
  async [GET_RECIPE]({ commit, state }, recipesId) {
    try {
      let recipe = state.recipes.find(r => r._id.$oid === recipesId);
      if (!recipe) {
        recipe = await fetchRecipe(recipesId);
      }
      commit(SET_RECIPE, recipe);
    } catch (error) {
      commit(SET_ERROR, error);
    }
  },
  async [GET_RECIPES]({ commit }, searchParams) {
    try {
      const { title, allergens } = searchParams;
      commit(SET_SEARCH_PARAMS, searchParams);
      const { recipes, stats } = await fetchRecipes(title, allergens);
      commit(SET_RECIPES, [recipes, stats]);
    } catch (error) {
      commit(SET_ERROR, error);
    }
  },
  async [GET_ALLERGENS]({ commit, state }) {
    if (state.allergens.length === 0) {
      try {
        const raw = await fetchAllergens();
        const allergens = raw.map(r => r.group);
        commit(SET_ALLERGENS, allergens);
      } catch (error) {
        commit(SET_ERROR, error);
      }
    }
  }
};

const mutations = {
  [SET_RECIPES](state, [recipes, stats]) {
    state.recipes = recipes;
    state.stats = stats;
  },
  [SET_ALLERGENS](state, allergens) {
    state.allergens = allergens;
  },
  [SET_SEARCH_PARAMS](state, searchParams) {
    state.searchParams = searchParams;
  },
  [SET_RECIPE](state, recipe) {
    state.recipe = recipe;
  }
};

export default {
  state,
  actions,
  mutations
};
