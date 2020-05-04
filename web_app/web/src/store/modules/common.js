import { CLEAR_ERROR, POPULATE_ERROR } from "../actions";
import { SET_ERROR } from "../mutations";

const state = {
  error: null
};

const getters = {
  error(state) {
    return state.error;
  }
};

const actions = {
  [CLEAR_ERROR]({ commit }) {
    commit(SET_ERROR, null);
  },
  [POPULATE_ERROR]({ commit }, error) {
    commit(SET_ERROR, error);
  }
};

const mutations = {
  [SET_ERROR](state, error) {
    const message = error.response.data;
    state.error = message;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
