<template>
  <div class="container">
    <div class="row h-100 w-auto justify-content-center text-center">
      <h1>Page des conseils</h1>
    </div>
    <div
      id="conseilForm"
      class="row h-100 w-auto justify-content-center text-center"
      v-show="isAuthenticated && loggedInUser.is_staff"
    >
      <ConseilForm button="Créer un conseil de quartier"></ConseilForm>
    </div>
    <div class="row justify-content-center">
      <ListOfProjects
        class="text-center"
        project_type="Conseil de quartier"
        my_projects="false"
        published="true"
        participated="false"
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
  padding-top: 13rem;
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
  .container #conseilForm {
    padding-bottom: 2rem;
  }
  .container {
    max-width: 50%;
    padding-top: 10rem;
    padding-bottom: 6rem;
    color: rgb(0, 14, 116);
  }
}
</style>
