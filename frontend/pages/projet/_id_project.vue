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
      <div class="row">
        <p>{{ this.project.description }}</p>
      </div>
      <div v-if="loaded">
        <div v-if="this.project.project_type !== petition_type_id">
          <div class="row" v-if="this.project.question.length != 0">
            <div v-if="userHasParticipated">
              <p>Vous avez déjà participé à ce sondage.</p>
            </div>
            <div v-else>
              <Questions
                :project="project"
                :user="loggedInUser.id"
                :questions="questions"
                v-on:hasparticipated="refresh()"
              />
            </div>
          </div>
        </div>
        <div
          class="column"
          v-bind="this.project"
          v-if="
            this.project.project_type === petition_type_id &&
              this.project.ready_for_publication
          "
        >
          <div v-if="userLikesProject">
            <b-button variant="primary" @click="cancelLikePetition()"
              >Ne plus supporter la pétition</b-button
            >
          </div>
          <div v-else>
            <b-button variant="primary" @click="likePetition()"
              >Soutenir la pétition</b-button
            >
          </div>
          <div v-if="userHasCommented">
            <p>Commentaire déjà posté</p>
          </div>
          <div v-else>
            <b-form-group label="Commenter la pétition" :state="commentState">
              <b-form-textarea
                id="user_comment"
                v-model="user_comment_input"
                :state="commentState"
              ></b-form-textarea>
              <b-button
                size="md"
                variant="primary"
                @click="handleSubmitComment()"
                >Poster mon commentaire</b-button
              >
            </b-form-group>
          </div>
          <div class="column">
            <h3>Commentaires</h3>
            <div
              v-for="comment in this.comments_published"
              :key="comment.id_comment"
            >
              {{ comment.owner }}
              {{ comment.text }}
              {{ comment.publication }}
            </div>
          </div>
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
    },
    userHasParticipated() {
      if (this.questions_answered.length > 0) {
        return true;
      } else {
        return false;
      }
    },
    userHasCommented() {
      if (this.comment_saved) {
        return true;
      }
      return false;
    },
    commentState() {
      if (this.user_comment_input.length === 0) {
        return false;
      } else if (this.user_comment_input === ' ') {
        return false;
      } else {
        return true;
      }
    }
  },
  data() {
    return {
      id_project: this.$route.params.id_project,
      project: null,
      questions: [],
      conseil_type_id: '',
      consultation_type_id: '',
      petition_type_id: '',
      questions_answered: [],
      loaded: false,
      comment_saved: null,
      user_comment_input: '',
      comments_published: []
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
    if (this.project.question.length > 0) {
      for (let question in this.project.question) {
        response = await this.$axios.get(this.project.question[question]);
        this.questions.push(response.data);
      }
    }
    for (const question in this.questions) {
      response = await fetch(
        `http://127.0.0.1:8000/user_answer/?question=${this.questions[question].id_question}&user=${this.loggedInUser.id}`
      ).then(res => res.json());
      if (typeof response[0] !== 'undefined') {
        this.questions_answered.push(response[0]);
      }
    }
    data = { owner: this.loggedInUser.id, project: this.id_project };
    response = await this.$axios.get('comment', { params: data });
    if (typeof response.data[0] !== 'undefined') {
      this.comment_saved = response.data[0]['id_comment'];
    }
    this.comments_published = [];
    data = { project: this.id_project };
    response = await this.$axios.get('comment', { params: data });
    if (typeof response.data[0] !== 'undefined') {
      for (const element in response.data) {
        this.comments_published.push(response.data[element]);
      }
    }
    this.loaded = true;
  },

  methods: {
    // Function used to add a like from the user to this petition
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

    // Function used to delete a like from the user to this petition
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
    },

    // Function refreshing the element
    refresh() {
      this.$nuxt.refresh();
    },

    // Function sending a post request to the API to create a comment
    async postComment() {
      const data = { project: this.id_project, text: this.user_comment_input };
      try {
        const response = await this.$axios.post('comment/', data);
        console.log(response.data);
      } catch (error) {
        console.log(error.data);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys];
        window.alert(errorMessage);
      }
    },

    async handleSubmitComment() {
      console.log('COMMENT STATE ', this.commentState);
      if (!this.commentState) {
        return;
      } else {
        await this.postComment();
      }
      this.$nuxt.refresh();
    }

    // // Function setting a delay of 2 seconds
    // async refresh2secondes() {
    //   const delay = ms => new Promise(res => setTimeout(res, ms));
    //   await delay(2000);
    // }
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
