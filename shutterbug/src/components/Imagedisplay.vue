<template>
    <div>
        <v-row class="Images">
            <v-col cols="4"  v-for="n in images.length" :key="n" >
                <v-card-media>
                    <v-img :src="String(images[n])" aspect-ratio="1" class=”image-fit”>
                    </v-img>
                </v-card-media>
            </v-col>
        </v-row>
    </div>
</template>

<script>
export default {
  data: () => ({
      images: localStorage.getItem("images").split(",")
  }),
  methods: {
    toggle() {
      this.showSection = !this.showSection
    }
  }
}
</script>

<style scoped>
.Images{
    width: 50%;
    position: absolute;
    transform: translateY(50%);
    transform: translateX(50%);
    margin-top: 120px;
    margin-bottom:10px;
}
.image-fit{
    height: 100%;
    width: 100%; 
    object-fit: cover;
    min-height: 100vh;
}
</style>