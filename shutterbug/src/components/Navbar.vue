<template>
  <nav>
    <v-toolbar>
      <v-toolbar-title class="">
          <v-btn  color="secondary"  class="btn" medium to="/">
            <span><h2>Shutterbug</h2></span>
          </v-btn>
         
        <router-view :key="$route.fullPath"></router-view>
      </v-toolbar-title>
      <v-spacer> </v-spacer>

      <v-btn color="secondary" class="btn" small v-if="token !== null" to="/Portfolio">
        <span><h2>Folders</h2></span>
      </v-btn>

      <v-btn color="secondary"  class="btn" small v-if="token !== null" to="/Logs">
        <span><h2>Logs</h2></span>
      </v-btn>

      <v-btn v-if="token != null" color="secondary"  class="btn" small @click="logout">
        <span><h2>Signout</h2></span>
      </v-btn>

      <v-btn v-else-if="token == null" color="secondary"  class="btn" small to="/Login">
        <span><h2>Login</h2></span>
      </v-btn>
      <v-switch 
          color="secondary"
          width = 5px 
          v-model="$vuetify.theme.dark"
          hint="Change the Theme to Dark Mode"
          label="Dark Mode"
          persistent-hint
          ></v-switch>
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
