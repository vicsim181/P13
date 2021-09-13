<template>
  <div>
    <CustomNavbar></CustomNavbar>
    <Login class="login"></Login>
    <CustomFooter></CustomFooter>
  </div>
</template>

<script>
export default { middleware: 'guest' };
</script>

<style>
.login {
  padding-top: 13rem;
  padding-bottom: 7rem;
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .login {
    padding-top: 18rem;
  }
}
</style>
