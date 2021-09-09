<template>
  <div>
    <CustomNavbar />
    <div v-if="this.project" v-bind="this.project" class="container">
      <div class="column" id="top">
        <strong
          ><h1>{{ this.project.name }}</h1></strong
        >
      </div>
      <div id="data">
        <div class="column">
          <h3 class="text-center">{{ this.project.place }}</h3>
        </div>
        <div class="column">
          <p class="pre-formatted">
            <u>Description du projet :</u> <br />{{ this.project.description }}
          </p>
          <br />
          <u v-if="project.project_type === conseil_type_id"
            >Date du conseil:</u
          >
          <u v-else>Prend fin le:</u> <br />{{ this.project.end_date }}
        </div>
      </div>
      <div v-if="loaded">
        <div
          v-if="
            this.project.project_type !== petition_type_id &&
              this.project.ready_for_publication
          "
        >
          <div id="form" v-if="this.project.question.length != 0">
            <div v-if="userHasParticipated">
              <p>Vous avez déjà participé à ce sondage.</p>
            </div>
            <div v-else>
              <Questions
                :project="project"
                :user="loggedInUser.id"
                :questions="questions"
                :mcqanswers="mcqanswers"
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
          <div id="like">
            <div v-if="userLikesProject">
              <b-button class="button" @click="cancelLikePetition()"
                >Ne plus supporter la pétition</b-button
              >
            </div>
            <div v-else>
              <b-button class="button" variant="primary" @click="likePetition()"
                >Soutenir la pétition</b-button
              >
            </div>
          </div>
          <div id="comment">
            <div v-if="userHasCommented">
              <p>Vous avez déjà commenté la pétition</p>
            </div>
            <div v-else>
              <b-form-group label="Commenter la pétition" :state="commentState">
                <b-form-textarea
                  id="user_comment"
                  v-model="user_comment_input"
                  :state="commentState"
                ></b-form-textarea>
                <b-button
                  class="button"
                  size="md"
                  @click="handleSubmitComment()"
                  >Poster mon commentaire</b-button
                >
              </b-form-group>
            </div>
          </div>
          <div class="column" id="comments">
            <b-button class="button" v-b-toggle.my-collapse
              >Voir les commentaires</b-button
            >
            <b-collapse
              title="Commentaires"
              id="my-collapse"
              v-for="comment in this.comments_published"
              :key="comment.id_comment"
            >
              <b-card class="comments">
                <b-card-text class="column">
                  <b-icon icon="person-fill"></b-icon>{{ comment.publication }}
                  <br />
                  {{ comment.text }}</b-card-text
                >
              </b-card>
            </b-collapse>
          </div>
        </div>
        <div v-if="!project.ready_for_publication" class="not_published">
          <div class="column">
            <ul
              v-for="question in questions_not_published"
              :key="question.id_question"
            >
              <li>
                {{ question[0].wording }}
                <b-button
                  size="sm"
                  class="button delete"
                  @click="handleDeleteQuestion(question[0].id_question)"
                  >Supprimer la question</b-button
                >
              </li>
              <div v-if="question[1].length > 0">
                <div
                  v-for="mcqanswer in question[1]"
                  :key="mcqanswer.id_answer"
                >
                  <ul>
                    <li>
                      {{ mcqanswer.wording }}
                    </li>
                  </ul>
                </div>
              </div>
            </ul>
          </div>
          <div class="column" v-if="project.project_type === conseil_type_id">
            <MyNotPublishedConseil
              :project_data="project"
              v-on:done="refresh()"
            />
          </div>
          <div
            class="column"
            v-if="project.project_type === consultation_type_id"
          >
            <MyNotPublishedConsultation
              :project_data="project"
              v-on:done="refresh()"
            />
          </div>
          <div class="column" v-if="project.project_type === petition_type_id">
            <MyNotPublishedPetition
              :project_data="project"
              v-on:done="refresh()"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-else class="not-found text-center">
      <h3>Le projet recherché n'existe pas.</h3>
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
      questions: {},
      questions_not_published: {},
      conseil_type_id: '',
      consultation_type_id: '',
      petition_type_id: '',
      questions_answered: [],
      loaded: false,
      comment_saved: null,
      user_comment_input: '',
      comments_published: [],
      nombre: null,
      mcqanswers: {}
    };
  },
  async fetch() {
    await this.fetchProjectData();
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
    await this.fetchQuestions();
    if (this.project.ready_for_publication) {
      await this.fetchQuestionsAnswered();
      await this.fetchCommentSaved();
      await this.fetchCommentsPublished();
    }
    this.loaded = true;
    // this.$nuxt.refresh();
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
    async refresh() {
      await this.fetchProjectData();
      await this.fetchQuestions();
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

    // Function called when a user decides to comment a petition
    async handleSubmitComment() {
      if (!this.commentState) {
        return;
      } else {
        await this.postComment();
      }
      this.$nuxt.refresh();
    },

    // Function called when a user wants to delete a question from one of his non published projects
    async handleDeleteQuestion(id) {
      await this.deleteQuestion(id);
    },

    // Function fetching the data of the project
    async fetchProjectData() {
      const response = await this.$axios.get(`project/${this.id_project}`);
      this.project = response.data;
    },

    // Function fecthing the questions to display for a non published project
    async fetchQuestions() {
      if (this.project.question.length > 0) {
        for (let question in this.project.question) {
          let response = await this.$axios.get(this.project.question[question]);
          let answers = [];
          let mcqanswers_wording = [];
          if (response.data['mcqanswer'].length > 0) {
            for (const mcqanswer in response.data['mcqanswer']) {
              const response_mcqanswer = await this.$axios.get(
                response.data['mcqanswer'][mcqanswer]
              );
              answers.push(response_mcqanswer.data);
              mcqanswers_wording.push(response_mcqanswer.data.wording);
            }
            this.mcqanswers[response.data.id_question] = mcqanswers_wording;
          }
          if (this.project.ready_for_publication) {
            this.questions[question] = [response.data, answers];
          } else {
            this.questions_not_published[question] = [response.data, answers];
          }
        }
      } else {
        this.questions_not_published = {};
        this.questions = {};
      }
    },

    // Function fetching the questions answered by the user, in order to check if the user has participated to this project
    async fetchQuestionsAnswered() {
      for (let question in Object.keys(this.questions)) {
        const data = {
          question: this.questions[question][0].id_question
        };
        try {
          const response = await this.$axios.get('user_answer', {
            params: data
          });
          console.log('RESPONSE ', response.data);
          if (typeof response.data[0] !== 'undefined') {
            this.questions_answered.push(response.data[0]);
          }
        } catch (error) {
          console.log(error.data);
        }
      }
      console.log('QUESTIONS ANSWERED ', this.questions_answered);
    },

    // Function fetching the comment saved by the user on this project, if there is one
    async fetchCommentSaved() {
      const data = { owner: this.loggedInUser.id, project: this.id_project };
      const response = await this.$axios.get('comment', { params: data });
      if (typeof response.data[0] !== 'undefined') {
        this.comment_saved = response.data[0]['id_comment'];
      }
    },

    // Function fetching the comments published if there are
    async fetchCommentsPublished() {
      this.comments_published = [];
      const data = { project: this.id_project };
      const response = await this.$axios.get('comment', { params: data });
      if (typeof response.data[0] !== 'undefined') {
        for (const element in response.data) {
          this.comments_published.push(response.data[element]);
        }
      }
    },

    // Function called when the user decides to delete a question on a not published project
    async deleteQuestion(id) {
      await this.$axios.delete(`question/${id}/`);
      this.questions = [];
      this.questions_not_published = {};
      this.refresh();
    }
  }
};
</script>

<style>
.container {
  padding-top: 8.4rem;
  padding-bottom: 10rem;
  min-width: 100%;
  padding-left: 0;
  padding-right: 0;
  color: rgb(0, 14, 116);
}
.not-found {
  padding-top: 13rem;
  color: rgb(0, 14, 116);
}
#top {
  background-color: rgb(0, 14, 116);
  color: whitesmoke;
  text-align: center;
  padding-top: 4rem;
  padding-bottom: 2rem;
}
#data {
  padding-top: 2rem;
  padding-bottom: 3.5rem;
  padding-left: 15rem;
  padding-right: 15rem;
  text-align: justify;
}
#data h3 {
  padding-bottom: 4rem;
}
#form {
  padding-left: 15rem;
}
#like {
  padding-left: 15rem;
  padding-bottom: 2rem;
}
.button {
  color: rgb(247, 247, 247);
  background-color: rgb(0, 14, 116);
}
.delete {
  margin-left: 1rem;
}
.button:hover {
  background-color: rgb(247, 247, 247);
  color: rgb(0, 14, 116);
}
.button:active {
  background-color: rgb(247, 247, 247);
  color: rgb(0, 14, 116);
}
#comment {
  padding-left: 15rem;
  padding-bottom: 2rem;
  padding-right: 15rem;
}
#comments {
  padding-left: 15rem;
  padding-bottom: 4rem;
  padding-right: 15rem;
}
.not_published {
  padding-bottom: 3.5rem;
  padding-left: 15rem;
  padding-right: 15rem;
  text-align: justify;
}
.pre-formatted {
  white-space: pre-wrap;
}
@media (min-width: 500px) and (max-width: 1200px) {
  .container {
    padding-top: 6rem;
  }
  #top {
    padding-top: 3.5rem;
  }
  #data {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
  }
  #data h3 {
    padding-bottom: 2rem;
  }
  #form {
    padding-left: 3rem;
  }
  #like {
    padding-left: 3rem;
    padding-bottom: 2rem;
  }
  #comment {
    padding-left: 3rem;
    padding-bottom: 2rem;
    padding-right: 3rem;
  }
  #comments {
    padding-left: 3rem;
    padding-bottom: 4rem;
    padding-right: 3rem;
  }
  .not_published {
    padding-bottom: 3.5rem;
    padding-left: 3rem;
    padding-right: 3rem;
    text-align: justify;
  }
}
@media (max-width: 499px) {
  .container {
    padding-top: 5rem;
  }
  #top {
    padding-top: 4rem;
  }
  #data {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
  }
  #data h3 {
    padding-bottom: 2rem;
  }
  #form {
    padding-left: 3rem;
  }
  #like {
    padding-left: 3rem;
    padding-bottom: 2rem;
  }
  #comment {
    padding-left: 3rem;
    padding-bottom: 2rem;
    padding-right: 3rem;
  }
  #comments {
    padding-left: 3rem;
    padding-bottom: 4rem;
    padding-right: 3rem;
  }
  .not_published {
    padding-bottom: 3.5rem;
    padding-left: 3rem;
    padding-right: 3rem;
    text-align: justify;
  }
}
</style>
