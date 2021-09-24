<template>
  <div>
    <div v-show="$auth.loggedIn">
      <h3>Vous êtes déjà connecté avec un compte.</h3>
    </div>
    <div v-show="!$auth.loggedIn">
      <Signup></Signup>
    </div>
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
