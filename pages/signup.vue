<template>
  <div>
    <Signup class="signup"></Signup>
  </div>
</template>

<script>
export default {
  middleware: "guest"
};
</script>

<style scoped>
.signup {
  padding-top: 13rem;
  padding-bottom: 6rem;
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .signup {
    padding-top: 10rem;
    padding-bottom: 7rem;
  }
}
@media (max-width: 1200px) {
  .signup {
    padding-top: 10rem;
    padding-bottom: 7rem;
  }
}
</style>