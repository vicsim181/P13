<template>
  <div>
    <Login class="login"></Login>
    <div class="row h-100 w-auto justify-content-center text-center">
      <nuxt-link to="signup/">Pas encore inscrit ? Cliquez ici.</nuxt-link>
    </div>
  </div>
</template>

<script>
export default { middleware: "guest" };
</script>

<style scoped>
.login {
  padding-top: 13rem;
  padding-bottom: 6rem;
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .login {
    padding-top: 10rem;
    padding-bottom: 2rem;
  }
}
@media (max-width: 1200px) {
  .login {
    padding-top: 10rem;
    padding-bottom: 2rem;
  }
}
</style>
