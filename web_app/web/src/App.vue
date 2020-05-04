<template>
  <v-app>
    <v-app-bar app dark style="background-color:#b3a369">
      <div class="d-flex align-center">
        <router-link :to="{ name: 'Home' }">
          <v-img
            alt="Georgia Tech Logo"
            contain
            :src="require('./assets/gt-logo.svg')"
            width="150"
          />
        </router-link>
      </div>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script>
import { mapState } from "vuex";
export default {
  watch: {
    error(message) {
      this.$notify.error({
        title: "Error",
        message,
        position: "bottom-left"
      });
    }
  },
  methods: {
    goHome() {
      this.$router.push("/");
    }
  },
  computed: {
    ...mapState({
      error: state => state.common.error
    })
  }
};
</script>
