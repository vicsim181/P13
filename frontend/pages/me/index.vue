<template>
  <!DOCTYPE html>
  <div>
    <CustomNavbar />
    <div class="container" v-if="isAuthenticated">
      <h1 class="row h-100 w-auto justify-content-center">Mon profil</h1>
      <div>
        <p>
          <strong>Prénom:</strong>
          {{ loggedInUser.first_name }}
        </p>
        <p>
          <strong>Nom de famille:</strong>
          {{ loggedInUser.last_name }}
        </p>
        <p>
          <strong>Adresse email:</strong>
          {{ loggedInUser.email }}
        </p>
        <p>
          <strong>Adresse postale:</strong>
          {{ loggedInUser.address[0] }}
        </p>
        <router-link
          :to="{
            name: 'me-mesconsultations'
          }"
          class="row h-100 w-auto ml-auto"
        >
          <strong>Mes consultations</strong>
        </router-link>
        <router-link
          :to="{
            name: 'me-mesconseils',
            params: {
              owner_id: loggedInUser.id,
              is_staff: loggedInUser.is_staff
            }
          }"
          class="row h-100 w-auto ml-auto"
        >
          <strong>Mes conseils de quartier</strong>
        </router-link>
        <router-link
          :to="{
            name: 'me-mespetitions',
            params: {
              owner_id: loggedInUser.id,
              is_staff: loggedInUser.is_staff
            }
          }"
          class="row h-100 w-auto ml-auto"
        >
          <strong>Mes pétitions</strong>
        </router-link>
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  }
};
</script>

<style>
.container {
  min-width: 100%;
  padding-top: 15rem;
  padding-bottom: 10rem;
  color: rgb(0, 14, 116);
}
@media (max-width: 1200px) {
  .container h1 {
    font-size: 2.5rem;
    margin-bottom: 3rem;
  }
  .container {
    padding-top: 13rem;
    padding-bottom: 13rem;
  }
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .container {
    padding-top: 18rem;
    padding-bottom: 13rem;
  }
}
</style>
