<template>
  <div v-if="isAuthenticated">
    <CustomNavbar></CustomNavbar>
    <h3>Vous êtes déjà connecté avec un compte.</h3>
    <CustomFooter></CustomFooter>
  </div>
  <div v-else>
    <CustomNavbar></CustomNavbar>
    <Signup></Signup>
    <CustomFooter></CustomFooter>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  auth: false
};
</script>

<style>
h3 {
  margin-top: 8rem;
  text-align: center;
}
</style>
