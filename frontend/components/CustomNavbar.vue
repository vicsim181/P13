<template>
  <b-navbar fixed="top" toggleable="xl" type="dark" variant="dark">
    <b-navbar-brand href="/" class="title">participons</b-navbar-brand>
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
        <b-nav-item-dropdown right v-if="isAuthenticated">
          <template #button-content>
            <h4 class="col-md-3 item">Mon compte</h4>
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
  padding-bottom: 1rem;
}
#nav-collapse {
  flex-direction: column;
  align-items: baseline;
  text-align: center;
  align-content: space-around;
}
.title {
  font-family: 'Verdana, sans-serif';
  font-weight: 700;
  font-size: 4.5rem;
  text-decoration-line: underline;
}
@media (max-width: 479px) {
  .title {
    font-size: 3rem;
  }
}
.navbar_elements {
  align-items: center;
  text-align: center;
  align-self: center;
}
.item {
  font-size: 1.8rem;
  text-shadow: 1px 1px 1px rgb(255, 255, 255), 0 0 10rem rgb(255, 255, 255),
    3rem 1rem 4rem rgb(255, 255, 255);
}
</style>
