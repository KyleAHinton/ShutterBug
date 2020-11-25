<template>
  <div>
    <v-row class="Images">
      <v-col cols="4" v-for="(n, index) in this.images.length" :key="n">
        <v-container>
          <v-hover v-slot="{ hover }">
            <v-card :elevation="hover ? 12 : 2" :class="{ 'on-hover': hover }">
              <v-img :src="images[index]" aspect-ratio="1" class="”image-fit”"></v-img>
              <v-btn
                :class="{ 'show-btns': hover }"
                color="transparent"
                @click="deleteImage(index)"
                >Delete</v-btn
              >
              <v-btn
                :class="{ 'show-btns': hover }"
                color="transparent"
                @click="download(images[index])"
                >Download</v-btn
              >
            </v-card>
          </v-hover>
        </v-container>
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
    imageIDs: [],
    i: 0,
    uid: localStorage.getItem("user-id"),
  }),
  methods: {
    Images(n) {
      axios
        .get(`http://127.0.0.1:8000/image/?id=${n}`, {})
        .then((resp) => {
          this.images.push(resp.data[0].url);
          this.imageIDs.push(n);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    portfolio() {
      axios
        .get(`http://127.0.0.1:8000/portfolio/?user=${this.uid}`)
        .then((resp) => {
          this.imageinfo = resp.data;
          for (var i = 0; i <= this.imageinfo.length; i++) {
            this.Images(this.imageinfo[i].photo);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    download(n) {
      axios({
        method: "get",
        url: n,
        responseType: "arraybuffer",
      })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "Image.png"); //or any other extension
          document.body.appendChild(link);
          link.click();
        })
        .catch(() => console.log("error occured"));
    },
    deleteImage(n) {
      console.log(this.imageIDs[n])
      axios
        .delete(`http://127.0.0.1:8000/portfolio/?photo=${this.imageIDs[n]}&user=${this.uid}`)
        .then((resp) => {
          this.images.splice(n, 1);
          console.log(n)
          console.log(resp)
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    this.portfolio();
  },
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
.v-card {
  transition: opacity 0.4s ease-in-out;
}

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
</style>
