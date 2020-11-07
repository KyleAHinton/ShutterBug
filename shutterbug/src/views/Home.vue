<template>
  <div class="Home">
    <Searchbar />
    <div>
    <Imagedisplay />
    </div>
  </div>
</template>

<script>

import Searchbar from "../components/Searchbar.vue";
import Imagedisplay from "../components/Imagedisplay";

export default {
  name: "Home",
  components: {
    Searchbar,
    Imagedisplay
  }
};
</script>

<style scoped>
.Searchbar {
  margin-bottom: 50px;
}
</style>