<template>
  <div class="Imageview">
    <Portfoliocomponent />
    <v-spacer></v-spacer>
    <div>
      <Imagecontrolpanel />
    </div>
  </div>
</template>

<script>

import Portfoliocomponent from "../components/Portfoliocomponent.vue";
import Imagecontrolpanel from "../components/Imagecontrolpanel";

export default {
  name: "PortfolioInfo",
  components: {
    Portfoliocomponent,
    Imagecontrolpanel
  }
};
</script>

<style scoped>
.Searchbar {
  margin-bottom: 50px;
}
</style>