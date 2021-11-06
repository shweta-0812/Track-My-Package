import axios from "axios";

const state = {
  parcelsList: [],
};

const actions = {
  async addNewParcel({ commit }, payload) {
    const newParcel = payload.parcel;
    const response = await axios.post(
      "http://localhost:8000/api/v1/parcel",
      newParcel
    );
    payload = { parcel: response.data };
    commit("setNewParcel", payload);
  },
  async fetchAllParcels({ commit }, payload) {
    const response = await axios.get("http://localhost:8000/api/v1/parcel");
    payload = { parcels: response.data };
    commit("setAllParcels", payload);
  },
  async fetchParcelById({ commit }, payload) {
    const parcelID = payload.parcelID;
    const response = await axios.get(
      "http://localhost:8000/api/v1/parcel/",
      parcelID
    );
    payload = { parcels: response.data };
    commit("setAllParcels", payload);
  },
};

const mutations = {
  setNewParcel: (state, payload) => state.parcel.unshift(payload.parcel),
  setAllParcels: (state, payload) => (state.parcelsList = payload.parcels),
};

const getters = {
  getParcels: (state) => state.parcelsList,
  getParcelById: (state) => (id) => {
    return state.parcelsList.find((parcel) => parcel.id === id);
  },
};

export default {
  state,
  mutations,
  actions,
  getters,
};
