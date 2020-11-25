<template>
  <div>
    <v-row class="Logs">
      <v-col cols="4" v-for="n in Object.keys(logs).length" :key="n.date">
        <v-container>
          <v-card v-on:click="edit(logs[Object.keys(logs)[n - 1]])">
            <v-card-title>{{ Object.keys(logs)[n - 1] }}</v-card-title>
            <v-card-text>{{
              logs[Object.keys(logs)[n - 1]].edits
            }}</v-card-text>
            <v-img :src="logs[Object.keys(logs)[n - 1]].url"></v-img>
          </v-card>
        </v-container>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    uid: localStorage.getItem("user-id"),
    logs: null,
  }),
  mounted() {
    axios
      .get(`http://127.0.0.1:8000/logs/?user_id=${this.uid}`)
      .then((resp) => {
        this.logs = resp.data;
      })
      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    edit(key) {
    console.log(key)
      axios
        .post(`http://127.0.0.1:8000/edit/`, {
            url: key.url,
            user_id: key.user_id,
            edits: key.edits
        })
        .then((resp) => {console.log(resp)        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.Logs {
  width: 50%;
  position: absolute;
  transform: translateY(50%);
  transform: translateX(50%);
  margin-top: 120px;
  margin-bottom: 10px;
  overflow-y: auto;
  max-height: 700px;
}
</style>