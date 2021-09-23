<template>
  <div class="container">
    <div class="row h-100 w-auto justify-content-center text-center">
      <h1>Page des consultations</h1>
    </div>
    <div
      id="consultationForm"
      class="row h-100 w-auto justify-content-center text-center"
      v-show="$auth.loggedIn && loggedInUser.is_staff"
    >
      <ConsultationForm button="Créer une consultation"></ConsultationForm>
    </div>
    <div class="row justify-content-center">
      <ListOfProjects
        class="text-center"
        project_type="Consultation"
        my_projects="false"
        published="true"
        participated="false"
        img="../static/consultation.jpg"
      ></ListOfProjects>
    </div>
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

<style scoped>
.container {
  min-width: 100%;
  padding-top: 6rem;
  padding-bottom: 6rem;
  color: rgb(0, 14, 116);
}
.container h1 {
  padding-bottom: 3rem;
}
@media (max-width: 1200px) {
  .container h1 {
    font-size: 2rem;
    padding-bottom: 1rem;
  }
  .container #consultationForm {
    padding-bottom: 2rem;
  }
  .container {
    max-width: 50%;
    padding-top: 5rem;
    padding-bottom: 6rem;
    color: rgb(0, 14, 116);
  }
}
</style>
