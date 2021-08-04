<template>
  <!DOCTYPE html>
  <div class="main">
    <CustomNavbar />
    <body>
      <div class="container">
        <h1 class="row h-100 w-auto justify-content-center">Mon profil</h1>
        <div class="content">
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
          <strong>Projets:</strong>
          <li
            v-for="project in loggedInUser.project"
            :key="project.id"
            class="row h-100 w-auto justify-items-center"
          >
            <ul>
              {{
                project
              }}
            </ul>
          </li>
          <!-- {{ loggedInUser.project }} -->
        </div>
      </div>
    </body>
    <CustomFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['loggedInUser'])
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
