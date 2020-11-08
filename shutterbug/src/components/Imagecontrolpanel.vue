<template>
    <v-footer class="footer">
      <!-- Download a photo, always available. -->
      <v-btn color="grey" class="btn" small @click="download()">
        <span>Download</span>
      </v-btn>
      <v-spacer></v-spacer>
      <!-- Save a photo, available if a photo has not yet been saved. -->
      <v-btn color="grey" class="btn" small>
        <span>Save</span>
      </v-btn>
      <v-spacer></v-spacer>
      <!-- Button to modify a given photo, available if that photo has been saved. -->
      <v-btn color="grey" class="btn" small>
        <span>Modify</span>
      </v-btn>
      <v-spacer></v-spacer>
      <!-- Button to delete the photo from a given user, if that user has saved said photo -->    
      <v-btn color="grey" class="btn" small>
        <span>Delete</span>
      </v-btn>
    </v-footer>
</template>

<script>

import axios from "axios";

export default {
    data: () => ({
      images: localStorage.getItem("images").split(",")
     }),
    methods: {
    download(){
      axios({
        method: 'get',
        url: String(this.images[Number(this.$route.params.id)]),
        responseType: 'arraybuffer'
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'Image.png') //or any other extension
        document.body.appendChild(link)
        link.click()
      })
      .catch(() => console.log('error occured'))
    }
  }
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

.footer{
    width: 50%;
    position: fixed;
    transform: translateY(50%);
    transform: translateX(50%);
    margin-top: 500px;
}
</style>
