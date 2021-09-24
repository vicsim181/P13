<template>
  <div>
    <Signup class="signup"></Signup>
  </div>
</template>

<script>
export default {
  auth: false,
  middleware: 'guest'
};
</script>

<style>
.signup {
  padding-top: 13rem;
  padding-bottom: 7rem;
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .signup {
    padding-top: 18rem;
  }
}
</style>
