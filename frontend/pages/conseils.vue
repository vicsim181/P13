<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="row h-100 w-auto justify-content-center text-center">
        <h1>Page des conseils</h1>
      </div>
      <div
        class="row h-100 w-auto justify-content-center text-center"
        v-if="isAuthenticated"
      >
        <ConseilForm v-if="loggedInUser.is_staff" />
      </div>
      <div class="row h-100 w-auto justify-content-center text-center">
        <ListOfConseils />
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  auth: false,
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  middleware: 'auth'
};
</script>

<style>
.container {
  min-width: 100%;
  padding-top: 15rem;
  padding-bottom: 10rem;
  color: rgb(0, 14, 116);
}
</style>
