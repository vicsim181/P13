<template>
  <!DOCTYPE html>
  <div>
    <CustomNavbar></CustomNavbar>
    <div class="container" v-if="isAuthenticated">
      <h1 class="row h-100 w-auto justify-content-center text-center">
        Mon profil
      </h1>
      <div id="data" class="text-center">
        <strong>Prénom:</strong>
        <p>{{ loggedInUser.first_name }}</p>
        <strong>Nom de famille:</strong>
        <p>
          {{ loggedInUser.last_name }}
        </p>
        <strong>Adresse email:</strong>
        <p>
          {{ loggedInUser.email }}
        </p>
        <strong>Adresse postale:</strong>
        <p v-if="loggedInUser.address[0]">{{ user_adress }}</p>
        <AddressForm v-else></AddressForm>
        <br />
        <b-button
          :to="{
            name: 'me-mesconsultations'
          }"
          class="button"
        >
          Mes consultations
        </b-button>
        <br />
        <b-button
          :to="{
            name: 'me-mesconseils',
            params: {
              owner_id: loggedInUser.id,
              is_staff: loggedInUser.is_staff
            }
          }"
          class="button"
        >
          Mes conseils de quartier
        </b-button>
        <br />
        <b-button
          :to="{
            name: 'me-mespetitions',
            params: {
              owner_id: loggedInUser.id,
              is_staff: loggedInUser.is_staff
            }
          }"
          class="button"
        >
          Mes pétitions
        </b-button>
      </div>
    </div>
    <CustomFooter></CustomFooter>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  data() {
    return {
      user_adress: ''
    };
  },
  async fetch() {
    if (this.loggedInUser.address[0]) {
      const response = await this.$axios.get(this.loggedInUser.address[0]);
      const address =
        response.data['num'] +
        ', ' +
        response.data['street'] +
        ' - ' +
        response.data['postal_code'] +
        ' ' +
        response.data['city'];
      this.user_adress = address;
    }
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
.button {
  color: rgb(247, 247, 247);
  background-color: rgb(0, 14, 116);
}
.button:hover {
  color: rgb(0, 14, 116);
  background-color: rgb(247, 247, 247);
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
