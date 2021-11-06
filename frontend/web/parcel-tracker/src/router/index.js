import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home";
// import Dashboard from "@/views/Dashboard";

import Callback from "@/views/Callback";
import ErrorPage from "@/views/Error";

// import { routeGuard } from "@/auth";
// import ParcelsList from "../views/ParcelsList";
import SignUp from "../views/SignUp";
import Login from "../views/Login";
// import PageNotFound from "../components/PageNotFound";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
  },
  // {
  //   path: "/dashboard",
  //   name: "Dashboard",
  //   component: Dashboard,
  //   beforeEnter: routeGuard,
  // },
  // {
  //   path: "/parcel",
  //   name: "Parcels",
  //   component: ParcelsList,
  //   beforeEnter: routeGuard,
  // },
  {
    path: "/callback",
    name: "Callback",
    component: Callback,
  },
  {
    path: "/error",
    name: "Error",
    component: ErrorPage,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ["/login", "/signup"];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem("user");
  if (authRequired && !loggedIn) {
    return next("/login");
  }
  next();
});

export default router;
