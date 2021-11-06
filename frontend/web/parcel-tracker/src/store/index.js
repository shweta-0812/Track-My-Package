import { createStore } from "vuex";
import parcelsStore from "../parcels";
import userStore from "../user";

export default createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    parcels: parcelsStore,
    user: userStore,
  },
});
