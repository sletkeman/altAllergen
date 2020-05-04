import Vue from "vue";
import App from "./App.vue";
import router from "./router.js";
import store from "./store";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);
const vuetify = new Vuetify({});

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
