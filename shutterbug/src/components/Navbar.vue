<template>
  <nav>
    <v-toolbar>
      <v-toolbar-title class="text-uppercase white--text">
          <v-btn color="grey" class="btn" medium to="/">
            <span>Shutterbug</span>
          </v-btn>
        <router-view :key="$route.fullPath"></router-view>
      </v-toolbar-title>
      <v-spacer> </v-spacer>

      <v-btn color="grey" class="btn" small v-if="token !== null">
        <span>Folders</span>
      </v-btn>

      <v-btn color="grey" class="btn" small v-if="token !== null">
        <span>Settings</span>
      </v-btn>

      <v-btn v-if="token != null" color="grey" class="btn" small @click="logout">
        <span>Signout</span>
      </v-btn>

      <v-btn v-else-if="token == null" color="grey" class="btn" small to="/Login">
        <span>Login</span>
      </v-btn>

    </v-toolbar>
  </nav>
</template>

<script>
export default {
  data: () => ({
      token: localStorage.getItem("user-token"),
      uid: localStorage.getItem("user-id"),
  }),
  methods: {
    logout() {
        localStorage.removeItem("user-token");
        this.token = null;
    },
  },
};
</script>

<style scoped>
.btn {
  margin-left: 20px;
}

.link {
  text-decoration: none;
  color: "inherit";
}
</style>
