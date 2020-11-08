<template>
  <div>
    <v-card class="form">
      <v-card-text>
        <v-card-title class="justify-center">
          Login
        </v-card-title>
        <v-form ref="loginForm" @submit.prevent="login" v-if="token == null">
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="loginUsername"
                label="Username"
                required
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="loginPassword"
                :type="showpass ? 'text' : 'password'"
                label="Password"
                counter
                @click:append="showpass = !showpass"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-btn size="medium" outlined type="submit" color="grey">
            Login
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm",
  data: () => ({
    showpass: false,
    username: "",
    password: "",
    token: null,
  }),
  methods: {
    login() {
      axios
        .post("http://127.0.0.1:8000/authenticate/", {
          username: this.loginUsername,
          password: this.loginPassword,
        })
        .then((resp) => {
          this.token = resp.data.token;
          localStorage.setItem("user-token", resp.data.token);
          localStorage.setItem("user-id", resp.data.id);
          this.$router.push('/');
        })
        .catch((err) => {
          localStorage.removeItem("user-token");
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
.form {
  width: 50%;
  position: absolute;
  transform: translateY(50%);
  transform: translateX(50%);
  margin-top: 50px;
}
</style>
