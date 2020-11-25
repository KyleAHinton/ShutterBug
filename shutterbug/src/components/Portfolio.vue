<template>
  <div>
    <v-row class="Images">
      <v-col cols="4" v-for="n in images" :key="n">
        <router-link :to="`/Portfolio/${n}/${localStorage.getItem(user - id)}`">
          <v-img :src="n" aspect-ratio="1" class="”image-fit”"></v-img>
        </router-link>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Portfolio",
  data: () => ({
    imageinfo: {},
    images: [],
    i: 0
  }),
  methods: {
    Images(n) {
      axios
        .get(`http://127.0.0.1:8000/image/?id=${n}`, {})
        .then(resp => {
          this.images.push(resp.data[0].url);
        })
        .catch(err => {
          console.log(err);
        });
    },
    portfolio() {
      axios
        .get(
          `http://127.0.0.1:8000/portfolio/?user=${localStorage.getItem(
            "user-id"
          )}`,
          {}
        )
        .then(resp => {
          this.imageinfo = resp.data;
          for (var i = 0; i < this.imageinfo.length; i++) {
            this.Images(this.imageinfo[i].photo);
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  beforeMount() {
    this.portfolio();
  }
};
</script>

<style scoped>
.Images {
  width: 50%;
  position: absolute;
  transform: translateY(50%);
  transform: translateX(50%);
  margin-top: 120px;
  margin-bottom: 60px;
  overflow-y: auto;
  max-height: 575px;
}
</style>
