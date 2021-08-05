<template>
  <!DOCTYPE html>
  <div class="main">
    <CustomNavbar />
    <body>
      <div class="container">
        <div class="row h-100 w-auto justify-content-center text-center">
          <h1>Page des consultations</h1>
        </div>
        <div class="row h-100 w-auto justify-content-center text-center" v-if="isAuthenticated">
          <p v-if="loggedInUser.is_staff"><ConsultationForm /></p>
        </div>
        <div class="row h-100 w-auto justify-content-center text-center">
          <p><Consultations /></p>
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
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
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
