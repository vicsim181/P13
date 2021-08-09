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
        <p>
          <strong>Membre du staff:</strong>
          {{ loggedInUser.is_staff }}
        </p>
        <router-link
          :to="{
            name: 'me-mesconsultations',
            params: { owner_id: loggedInUser.id }
          }"
          class="row h-100 w-auto"
        >
          <strong>Mes consultations</strong>
        </router-link>
        <router-link
          :to="{
            name: 'me-mesconseils',
            params: { owner_id: loggedInUser.id }
          }"
          class="row h-100 w-auto"
        >
          <strong>Mes conseils de quartier</strong>
        </router-link>
        <router-link
          :to="{
            name: 'me-mespetitions',
            params: { owner_id: loggedInUser.id }
          }"
          class="row h-100 w-auto"
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
</style>
