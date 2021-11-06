<template>
  <div class="w-flex row">
    <ul class="w-flex column pa10">
      <li v-for="parcel in getParcels" :key="parcel.id">
        <div class="w-flex row align-start justify-space-around">
          <p>{{ parcel.id }}</p>
          <p>{{ parcel.status }}</p>
          <!--          <small class="text-danger delete" @click="deleteUser(user.id)"-->
          <!--            >&#10005;</small-->
          <!--          >-->
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  name: "ParcelsList",
  computed: {
    ...mapGetters(["getParcels"]),
  },
  methods: {
    ...mapActions(["fetchAllParcels"]),
  },
  created() {
    this.fetchAllParcelsTracking();
  },
};
</script>
