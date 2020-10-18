<template>
  <v-app>
    <v-main>
      <Navbar />
      <Searchbar />
    </v-main>
  </v-app>
</template>

<script>
import Navbar from "./components/Navbar";
import Searchbar from "./components/Searchbar"

export default {
  name: "App",

  components: {
    Navbar,
    Searchbar
  },

  data: () => ({
    //
  })
};
</script>
