import { createRouter, createWebHashHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import CustomerPage from "./pages/CustomerPage.vue";

const routes = [
  { path: "/", component: HomePage },
  {
    path: "/customers/:id",
    component: CustomerPage,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
