<template>
  <div>
    <HomeMenu />
    <div class="main-container">
      <div class="loginsuccess-container">
        <h2 class="heading">Login Success!</h2>
        <div>
          <div v-if="LoggedinUserInfo.loginType === 'google'">
            <div class="center">
              <p>Welcome {{ LoggedinUserInfo.google.user.name }} !</p>
              <p>
                Email Address:
                {{ LoggedinUserInfo.google.user.email }} !
              </p>
              <img :src="LoggedinUserInfo.google.user.profileImage" />
              <p>
                <b>Google Access Token- </b
                >{{ LoggedinUserInfo.google.auth.access_token }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HomeMenu from "@/components/Menu";
import { mapGetters } from "vuex";

export default {
  name: "home",
  components: {
    HomeMenu,
  },
  computed: {
    ...mapGetters({
      LoggedinUserInfo: "getLoginUserInfo",
    }),
  },
};
</script>
