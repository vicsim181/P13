<template>
  <div>
    <CustomNavbar />
    <div v-if="this.project" v-bind="this.project" class="container">
      <div class="row">
        <p>{{ this.project.name }}</p>
      </div>
      <div class="row">
        <p>{{ this.project.place }}</p>
      </div>
      <div v-if="this.project.project_type !== petition_type_id">
        <div class="row" v-if="this.project.question.length != 0">
          <p>Questions:</p>
          <p>{{ this.project.question }}</p>
        </div>
      </div>
      <div
        class="row"
        v-bind="this.project"
        v-if="this.project.project_type === petition_type_id"
      >
        <div v-if="userLikesProject">
          <b-button @click="cancelLikePetition()"
            >Ne plus supporter la pétition</b-button
          >
        </div>
        <div v-else>
          <b-button @click="likePetition()">Soutenir la pétition</b-button>
        </div>
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser']),
    userLikesProject() {
      return this.project.liked_by.some(
        liker => liker.id === this.loggedInUser.id
      );
    }
  },
  data() {
    return {
      id_project: this.$route.params.id_project,
      project: null,
      questions: [],
      conseil_type_id: '',
      consultation_type_id: '',
      petition_type_id: ''
      // user_likes_project: this.userLikesProject
    };
  },
  async fetch() {
    this.project = await fetch(
      `http://127.0.0.1:8000/project/${this.id_project}`
    ).then(res => res.json());
    let data = { name: 'Conseil de quartier' };
    let response = await this.$axios.get('project_type', { params: data });
    let type_id = response.data['id_project_type'];
    this.conseil_type_id = type_id;
    data = { name: 'Pétition' };
    response = await this.$axios.get('project_type', { params: data });
    type_id = response.data['id_project_type'];
    this.petition_type_id = type_id;
    data = { name: 'Consultation' };
    response = await this.$axios.get('project_type', { params: data });
    type_id = response.data['id_project_type'];
    this.consultation_type_id = type_id;
  },
  methods: {
    async likePetition() {
      const data = { project_id: this.id_project, action: 'add' };
      try {
        const response = await this.$axios.put('like', data);
        console.log(response.data);
      } catch (error) {
        console.log(error.response);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
      this.$nuxt.refresh();
    },
    async cancelLikePetition() {
      const data = { project_id: this.id_project, action: 'delete' };
      try {
        const response = await this.$axios.put('like', data);
        console.log(response.data);
      } catch (error) {
        console.log(error.response);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
      this.$nuxt.refresh();
    }
  }
};
</script>

<style>
.container {
  padding-top: 13rem;
}
@media (min-width: 1200px) and (max-width: 1565px) {
  .container {
    padding-top: 18rem;
  }
}
</style>
