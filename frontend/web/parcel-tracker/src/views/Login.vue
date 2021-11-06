<template>
  <div class="main-container">
    <form>
      <div class="box-container">
        <h2 class="heading">Sign up With</h2>
        <SocialSignUp />
        <div>
          <p class="center">
            By signing up you agree to the
            <a href="#">Terms of Service</a>.
          </p>
        </div>
      </div>
    </form>
    <div class="footer">
      <p>Already have an account? <a href="/login"> Sign In</a></p>
    </div>
  </div>
</template>

<script>
import SocialSignUp from "../components/SocialLogin";
export default {
  name: "signup",
  components: {
    SocialSignUp,
  },
};
</script>
