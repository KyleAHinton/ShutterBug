<template>
  <div class="Image">
    <img :src="String(this.images[Number(this.$route.params.id)])">
  </div>
</template>

<script>
export default {
  data: () => ({
      images: localStorage.getItem("images").split(",")
  }),
};
</script>

<style scoped>
.Image {
  width: 60%;
  position: absolute;
  transform: translateY(50%);
  transform: translateX(50%);
  margin-top: 50px;
}
</style>