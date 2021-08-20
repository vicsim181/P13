<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="h-100 justify-content-center text-center">
        <h1>Mes conseils de quartier</h1>
      </div>
      <br />
      <div class="text-center">
        <b-button
          @click="
            (activeTab = 'MyProjectsParticipated'),
              (welcome = false),
              (showspinner = true),
              (participatedState = true),
              (publishedState = false),
              (notPublishedState = false)
          "
          :pressed="participatedState"
          >Les conseils de quartier auxquelles j'ai participé</b-button
        >
        <b-button
          @click="
            (activeTab = 'MyProjectsPublished'),
              (welcome = false),
              (showspinner = true),
              (participatedState = false),
              (publishedState = true),
              (notPublishedState = false)
          "
          v-if="loggedInUser.is_staff"
          :pressed="publishedState"
          >Mes conseils de quartier publiés</b-button
        >
        <b-button
          @click="
            (activeTab = 'MyProjectsNotPublished'),
              (welcome = false),
              (showspinner = true),
              (participatedState = false),
              (publishedState = false),
              (notPublishedState = true)
          "
          v-if="loggedInUser.is_staff"
          :pressed="notPublishedState"
          >Mes conseils de quartier non publiés</b-button
        >
      </div>
      <div class="text-center">
        <b-spinner
          id="spinner"
          style="width: 6rem; height: 6rem;"
          label="Large Spinner"
          v-if="showspinner"
        ></b-spinner>
        <Component
          :is="activeTab"
          project_type="Conseil de quartier"
          v-on:loaded="loading()"
        />
        <h3 v-if="welcome && loggedInUser.is_staff" id="welcome">
          Choisissez les conseils que vous souhaitez consulter
        </h3>
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import MyProjectsParticipated from '../../components/MyProjectsParticipated.vue';
import MyProjectsPublished from '../../components/MyProjectsPublished.vue';
import MyProjectsNotPublished from '../../components/MyProjectsNotPublished.vue';

export default {
  auth: false,
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  components: {
    MyProjectsParticipated,
    MyProjectsPublished,
    MyProjectsNotPublished
  },
  data() {
    return {
      welcome: true,
      showspinner: false,
      activeTab: '',
      participatedState: false,
      publishedState: false,
      notPublishedState: false
    };
  },
  methods: {
    async loading() {
      const delay = ms => new Promise(res => setTimeout(res, ms));
      await delay(2000);
      this.showspinner = false;
    }
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
#spinner {
  margin-top: 10rem;
}
#welcome {
  padding-top: 6rem;
}
.active {
  background: rgb(0, 14, 116) !important;
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
