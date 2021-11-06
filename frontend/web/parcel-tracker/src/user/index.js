import { setStore, getStore } from "@/config/utils";

const user = getStore("user");

const state = {
  loginUser: user,
};

const mutations = {
  setLoginUser(state, user) {
    state.loginUser = user;
    setStore("user", user);
  },
};
const actions = {};

const getters = {
  getLoginUserInfo(state) {
    return state.loginUser;
  },
};

export default {
  state,
  actions,
  mutations,
  getters,
};
