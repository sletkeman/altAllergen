import Vue from "vue";
import Vuex from "vuex";

import common from "./modules/common";
import recipe from "./modules/recipe";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    common,
    recipe
  }
});
