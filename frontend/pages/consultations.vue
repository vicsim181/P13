<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="h-100 justify-content-center text-center">
        <h1>Page des consultations</h1>
      </div>
      <div class="h-100 justify-content-center" v-if="isAuthenticated">
        <ConsultationForm v-if="loggedInUser.is_staff" />
      </div>
      <br />
      <div>
        <ListOfProjects
          project_type="Consultation"
          my_projects="false"
          published="true"
          participated="false"
        />
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
