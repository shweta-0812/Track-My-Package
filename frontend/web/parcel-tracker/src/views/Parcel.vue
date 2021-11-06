<template>
  <div class="home">
    <ParcelsList />
  </div>
</template>

<script>
// @ is an alias to /src
import ParcelsList from "./ParcelsList.vue";
export default {
  name: "Home",
  components: {
    ParcelsList,
  },
};
</script>
