<template>
  <!DOCTYPE html>
  <div class="main">
    <CustomNavbar />
    <body>
      <div class="container">
        <div class="row h-100 w-auto justify-content-center text-center">
          <h1>Page des pétitions</h1>
        </div>
        <div class="row h-100 w-auto justify-content-center text-center" v-if="isAuthenticated">
          <p>Créer une pétition</p>
        </div>
      </div>
    </body>
    <CustomFooter />
  </div>
</template>
<script>
import { mapGetters } from 'vuex';
export default { auth: false,
computed: {
    ...mapGetters(['isAuthenticated'])
  },
  middleware: 'auth'
};
</script>
<style>
body {
  min-width: 100%;
  padding-top: 6rem;
  padding-bottom: 7rem;
  color: rgb(0, 14, 116);
}
</style>
