<template>
  <div class="Imageview">
    <Imagecomponent />
    <v-spacer></v-spacer>
    <div>
      <Imagecontrolpanel />
    </div>
  </div>
</template>

<script>

import Imagecomponent from "../components/Imagecomponent.vue";
import Imagecontrolpanel from "../components/Imagecontrolpanel";

export default {
  name: "ImageView",
  components: {
    Imagecomponent,
    Imagecontrolpanel
  }
};
</script>

<style scoped>
.Searchbar {
  margin-bottom: 50px;
}
</style>