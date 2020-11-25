<template>
  <v-footer class="footer">
    <!-- Download a photo, always available. -->
    <v-btn color="grey" class="btn" @click="download()">
      <span>Download</span>
    </v-btn>
    <v-spacer></v-spacer>
    <!-- Save a photo, available if a photo has not yet been saved. -->
    <v-btn color="grey" class="btn" @click="image()">
      <span>Save</span>
    </v-btn>
    <v-text-field
      v-model="tags"
      label="Photo Tags"
      outlined
      filled
      small
      clearable
    >
    </v-text-field>
    <!-- Button to modify a given photo, available if that photo has been saved. -->
    <!-- Button to delete the photo from a given user, if that user has saved said photo -->
    <v-btn color="grey" class="btn">
      <span>Delete</span>
    </v-btn>
    <!-- Tag field, when tags are entered and then saved, they are included with the request to the portfolio API -->
    <v-btn color="grey" class="btn" @click="resize(String(images[Number($route.params.id)]))">
      <span>Resize</span>
    </v-btn>
    <v-text-field
      v-model="imgWidth"
      :label="this.imgwidth"
      outlined
      filled
      small
      clearable
    >
    </v-text-field>

    <v-text-field
      v-model="imgHeight"
      :label="this.imgheight"
      outlined
      filled
      small
      clearable
    >
    </v-text-field>
  </v-footer>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    images: localStorage.getItem("images").split(","),
    uid: localStorage.getItem("user-id"),
    imgheight: 0,
    imgwidth: 0,
  }),
    mounted() {
      var url = String(this.images[Number(this.$route.params.id)]);
      var img = new Image();
      img.src = url;
      this.imgheight = img.height;
      this.imgwidth = img.width;
    },
  methods: {
    download() {
      axios({
        method: "get",
        url: String(this.images[Number(this.$route.params.id)]),
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
    portfolio(response) {
      axios
        .post("http://127.0.0.1:8000/portfolio/", {
          user: this.uid,
          photo: response,
          tags: this.tags,
        })
        .then((resp) => {
          console.log(resp);
          this.$router.push("/Portfolio/");
        })
        .catch((err) => {
          console.log(err);
        });
    },
    image() {
      axios
        .post("http://127.0.0.1:8000/image/", {
          url: String(this.images[Number(this.$route.params.id)]),
        })
        .then((resp) => {
          this.portfolio(resp.data.id);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    resize(image) {
      axios
      .post("http://127.0.0.1:8000/edit/", {
        url: image,
				user_id: this.uid,
				edits: {
					resize: [parseInt(this.imgWidth), parseInt(this.imgHeight)]
				}
      })
      .then(() => {
        this.$router.push("Portfolio/");
      })
    }
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

.footer {
  width: 50%;
  position: fixed;
  transform: translateY(50%);
  transform: translateX(50%);
  margin-top: 500px;
}
</style>
