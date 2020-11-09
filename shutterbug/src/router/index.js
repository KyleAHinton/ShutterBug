import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
import Imageview from "../views/Imageview.vue"
import PortfolioView from "../views/PortfolioView.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/Login",
    name: "Login",
    component: Login
  },
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/Image/:id",
    name: "Images",
    component: Imageview
  },
  {
    path: "/Portfolio",
    name: "PortfolioView",
    component: PortfolioView
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
