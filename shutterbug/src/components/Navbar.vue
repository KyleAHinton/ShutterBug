<template>
    <nav>
        <v-toolbar>
            <v-toolbar-title class="text-uppercase white--text">
                <span>Shutterbug</span>
            </v-toolbar-title>
            <v-spacer>
            </v-spacer>

            <v-btn color="grey" class="btn" small>
                <span>Folders</span>
            </v-btn>
            <v-btn color="grey" class="btn" small>
                <span>Settings</span>
            </v-btn>
            <v-btn color="grey" class="btn" small>
                <span>Sign Out</span>
            </v-btn>
        </v-toolbar>
    </nav>
</template>

<script>
export default {
    
}
</script>

<style scoped>
.btn{
    margin-left: 20px;
}
</style>