import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import "./assets/css/login_signup.css";

import GoogleAuth from "./config/google_oauth.js";
const gauthOption = {
  clientId:
    "849459040053-ugt805bktide4o8pd57ma2nhu352lg8s.apps.googleusercontent.com",
  scope: "profile email",
  prompt: "select_account",
};

let app = createApp(App).use(store).use(router).use(GoogleAuth, gauthOption);
app.config.devtools = true;

app.mount("#app");