<template>
    <div class="searchbar">
        <v-text-field
        label="Image Search"
        clearable
        outlined
        dense
        filled
        hint="Descriptive words or key words for images."
        >
        </v-text-field>
    </div>
</template>

<script>
export default {
    name: "Searchbar",
}
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