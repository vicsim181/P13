<template>
  <div class="container">
    <div class="h-100 justify-content-center text-center">
      <h1>Mes conseils de quartier</h1>
    </div>
    <div
      class="h-100 justify-content-center text-center"
      v-if="!loggedInUser.is_staff"
    >
      <h3>Les conseils de quartier auxquels j'ai participé</h3>
    </div>
    <br />
    <div v-if="loggedInUser.is_staff">
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
          v-show="showspinner"
        ></b-spinner>
        <Component
          :is="activeTab"
          project_type="Conseil de quartier"
          v-on:loaded="loading()"
        ></Component>
        <h3 v-show="welcome" id="welcome">
          Choisissez les conseils que vous souhaitez consulter
        </h3>
      </div>
    </div>
    <div v-else>
      <MyProjectsParticipated
        project_type="Conseil de quartier"
      ></MyProjectsParticipated>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import MyProjectsParticipated from "../../components/MyProjectsParticipated.vue";
import MyProjectsPublished from "../../components/MyProjectsPublished.vue";
import MyProjectsNotPublished from "../../components/MyProjectsNotPublished.vue";
export default {
  computed: {
    ...mapGetters(["isAuthenticated", "loggedInUser"])
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
      activeTab: "",
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
  middleware: "auth"
};
</script>

<style scoped>
.container {
  min-width: 100%;
  padding-top: 13rem;
  padding-bottom: 6rem;
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
    padding-top: 10rem;
    padding-bottom: 9rem;
    color: rgb(0, 14, 116);
  }
  #welcome {
    padding-top: 3rem;
  }
  #spinner {
    margin-top: 3rem;
  }
}
</style>