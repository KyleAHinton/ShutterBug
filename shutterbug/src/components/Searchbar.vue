<template>
  <div>
    <v-form ref="searchbar" @submit.prevent="query()" class="searchbar">
        <v-text-field
        v-model="searchQuery"
        label="Image Search"
        >
        </v-text-field>
    </v-form>
  </div>
</template>

<script>

import axios from "axios";

export default {
  name: "SearchForm",
  data: () => ({
    images: {},
  }),
  methods: {
    query() {
      axios
        .get("http://127.0.0.1:8000/search/?query=", {
            params: {
                query: this.searchQuery
            }
        })
        .then((resp) => {
          localStorage.setItem("images", resp.data.image_urls);
          this.images = resp.data.image_urls;
          location.reload();
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.searchbar{
    width: 50%;
    position: absolute;
    transform: translateY(50%);
    transform: translateX(50%);
    margin-top: 50px
}
</style>