<template>
  <b-navbar fixed="top" toggleable="xl" type="dark" variant="dark">
    <b-navbar-brand href="/"
      ><img class="responsive_img" src="../static/logo.png"
    /></b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="navbar_elements row">
        <b-nav-item href="/consultations" class="col-md-3 item"
          ><b>CONSULTATIONS</b></b-nav-item
        >
        <b-nav-item href="/petitions" class="col-md-3 item"
          ><b>PETITIONS</b></b-nav-item
        >
        <b-nav-item href="/conseils" class="col-md-3 item"
          ><b>CONSEIL DE QUARTIER</b></b-nav-item
        >
        <b-nav-item-dropdown right v-if="isAuthenticated" no-caret>
          <template #button-content>
            <p class="col-md-3 item"><b>MON COMPTE</b></p>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              fill="whitesmoke"
              class="bi bi-caret-down-square-fill"
              viewBox="0 0 16 16"
            >
              <path
                d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2zm4 4a.5.5 0 0 0-.374.832l4 4.5a.5.5 0 0 0 .748 0l4-4.5A.5.5 0 0 0 12 6H4z"
              />
            </svg>
          </template>
          <b-dropdown-item href="/me">Mon Profil</b-dropdown-item>
          <b-dropdown-item href="#" @click="logout"
            >Me déconnecter</b-dropdown-item
          >
        </b-nav-item-dropdown>
        <b-nav-item href="/login" class="col-md-3 item" v-else
          ><b>Se connecter / S'inscrire</b></b-nav-item
        >
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  methods: {
    async logout() {
      await this.$auth.logout();
      this.$router.push('/');
      this.$nuxt.refresh();
    }
  }
};
</script>

<style>
.navbar {
  align-items: baseline;
  background-image: linear-gradient(
      rgba(194, 194, 191, 0.7),
      rgba(39, 39, 41, 0.8)
    ),
    url('https://media-public.canva.com/c7iQ8/MADyQ3c7iQ8/1/s3.jpg');
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
  flex-wrap: wrap;
  padding-bottom: 1.2rem;
}
#nav-collapse {
  flex-direction: column;
  align-items: baseline;
  text-align: center;
  align-content: space-between;
}
.navbar_elements {
  justify-content: space-evenly;
  align-items: center;
  text-align: center;
  align-self: center;
}
.item {
  font-size: 2rem;
  text-shadow: 1px 1px 1px rgb(255, 255, 255), 0 0 10rem rgb(255, 255, 255),
    3rem 1rem 4rem rgb(255, 255, 255);
}
.responsive_img {
  max-width: 100%;
  height: auto;
}
/* Doesn't influence the 8px padding on a.nav-link element of the navbar in the browser */
.nav-link {
  padding: 0rem;
}
@media (max-width: 1200px) {
  .item {
    font-size: 1.3rem;
  }
  .toggeable {
    size: 2px;
  }
  .responsive_img {
    max-width: 70%;
    height: auto;
  }
}
@media (min-width: 1200px) and (max-width: 1265px) {
  .item {
    font-size: 1.4rem;
  }
}
@media (min-width: 1265px) and (max-width: 1565px) {
  .item {
    font-size: 1.5rem;
  }
}
</style>
