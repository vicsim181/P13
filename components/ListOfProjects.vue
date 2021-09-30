<template>
  <div v-show="loaded">
    <div v-show="projects.length > 0" class="project">
      <b-card-group
        v-for="project in projects"
        :key="project.id_project"
        class="group"
      >
        <b-card
          :img-src="image"
          img-alt="Image"
          img-top
          tag="article"
          class="card"
        >
          <b-card-title style="text-align: center; height:2rem">{{
            project.name
          }}</b-card-title>
          <div class="card-body d-flex flex-column">
            <ul class="list-unstyled mt-3 mb-4">
              <li>
                <b-card-text id="description" class="pre-formatted">{{
                  project.description
                }}</b-card-text>
              </li>
              <br />
              <li>
                <b-card-text>
                  Publié le: {{ project.publication }}
                </b-card-text>
              </li>
              <li>
                <b-card-text v-show="project_type === 'Conseil de quartier'">
                  Date du conseil: {{ project.end_date }}
                </b-card-text>
                <b-card-text v-show="project_type !== 'Conseil de quartier'">
                  Prend fin le: {{ project.end_date }}
                </b-card-text>
              </li>
              <div v-show="project_type === 'Pétition'">
                <li>
                  <b-icon icon="hand-thumbs-up"></b-icon>
                  {{ project.liked_by.length }}
                </li>
              </div>
            </ul>
            <b-button
              squared
              class="align-self-end btn btn-lg btn-block button"
              style="margin-top: auto;"
              :to="`/projet/${project.id_project}`"
              >Consulter</b-button
            >
          </div>
        </b-card>
      </b-card-group>
    </div>
    <div v-show="projects_participated.length > 0" class="noresult">
      <p>Vous avez répondu au sondage du/des projet(s) suivant(s):</p>
      <ul
        v-for="project in projects_participated"
        :key="project.id_project"
        style="list-style-type:none;"
      >
        <li>
          <a :href="`/projet/${project.id_project}`">{{ project.name }}</a>
        </li>
      </ul>
    </div>
    <div v-show="projects_liked.length > 0" class="noresult">
      <p>Vous avez liké le(s) projet(s) suivant(s):</p>
      <ul
        v-for="project in projects_liked"
        :key="project.id_project"
        style="list-style-type:none;"
      >
        <li>
          <a :href="`/projet/${project.id_project}`">{{ project.name }}</a>
        </li>
      </ul>
    </div>
    <div v-show="projects_commented.length > 0" class="noresult">
      <p>Vous avez commenté le(s) projet(s) suivant(s):</p>
      <ul
        v-for="project in projects_commented"
        :key="project.id_project"
        style="list-style-type:none;"
      >
        <li>
          <a :href="`/projet/${project.id_project}`">{{ project.name }}</a>
        </li>
      </ul>
    </div>
    <div
      v-show="
        projects.length === 0 &&
          projects_commented.length === 0 &&
          projects_participated.length === 0 &&
          projects_liked.length === 0
      "
      class="noresult"
    >
      <p>Aucun projet de ce type.</p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  props: ['project_type', 'my_projects', 'published', 'participated'],
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  data() {
    return {
      image: null,
      loaded: false,
      project_type_id: null,
      petition_type_id: '',
      conseil_type_id: '',
      consultation_type_id: '',
      projects: [],
      projects_participated: [],
      projects_liked: [],
      projects_commented: []
    };
  },
  methods: {
    async getProjectType() {
      const data = { name: this.project_type };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    },
    onlyUnique(value, index, self) {
      return self.indexOf(value) === index;
    },
    //  ADD FUNCTION TO CALL NEW VIEW FOR NON PUBLISHED PROJECTS
    // Function sending a request to the API to get the published projects created by the user
    async getMyPublishedProjects() {
      const data = {
        project_type: this.project_type_id,
        owner_id: this.loggedInUser.id
      };
      try {
        const res = await this.$axios.get('project', { params: data });
        console.log('PROJECTS ', res.data);
        return res.data;
      } catch (error) {
        return [];
      }
    },
    // Function sending a request to the API to get the not published projects created by the user
    async getMyNOTPublishedProjects() {
      const data = {
        project_type: this.project_type_id,
        owner_id: this.loggedInUser.id
      };
      try {
        const res = await this.$axios.get('not_published', {
          params: data
        });
        return res.data;
      } catch (error) {
        return [];
      }
    },
    // Function sending a request to the API to get the projects for which the user has participated (answering the question(s) of the form)
    async getProjects() {
      const data = {
        project_type: this.project_type_id
      };
      try {
        const res = await this.$axios.get('project', { params: data });
        return res.data;
      } catch (error) {
        return [];
      }
    },
    // Function sending a request to the API to get the projects liked by the user
    async getProjectsLiked() {
      const data = {
        liked_by: this.loggedInUser.id
      };
      try {
        const res = await this.$axios.get('project', { params: data });
        return res.data;
      } catch (error) {
        return [];
      }
    },
    // Function sending a request to the API to get the projects commented by the user
    async getProjectsCommented() {
      const data = { owner: this.loggedInUser.id };
      const response = await this.$axios.get('comment/', { params: data });
      return response.data;
    },
    // Function sending a request to the API to get the answers of the user to the different forms
    async getUserAnswers() {
      // const data = { owner: this.loggedInUser.id };
      const response = await this.$axios.get('user_answer/');
      return response.data;
    },
    // Function sending a request to the API to get the questions to which the user answered
    async getQuestionsAnswered(response, element) {
      return await this.$axios.get(`question/${response[element].question}`);
    },
    // Function sending a request to the API to get the project to which the user answered
    async getProject(id_project) {
      return await this.$axios.get(`project/${id_project}`);
    },
    // Function sorting out the comments obtained through a request to the API
    async sortComments(comments) {
      if (comments.length !== 0) {
        for (const comment in comments) {
          if (
            !this.projects_commented.some(
              element => element.project == comments[comment].project
            )
          ) {
            const project = await this.getProject(comments[comment].project);
            this.projects_commented.push(project.data);
          }
        }
      }
    },
    // Function sorting the answers of the user and iterating throug the attached questions to find the concerned project
    async sortUserAnswers(response) {
      if (response.length !== 0) {
        for (const element in response) {
          const question = await this.getQuestionsAnswered(response, element);
          const project = await this.getProject(question.data.project);
          if (
            project.data.project_type === this.project_type_id &&
            !this.projects_participated.some(
              element => element.id_project == project.data.id_project
            )
          ) {
            this.projects_participated.push(project.data);
          }
        }
      }
    },
    async setImage() {
      if (this.project_type_id === this.consultation_type_id) {
        this.image = require('../static/consultation.jpg');
      } else if (this.project_type_id === this.petition_type_id) {
        this.image = require('../static/petition.jpeg');
      } else if (this.project_type_id === this.conseil_type_id) {
        this.image = require('../static/conseil.jpg');
      }
    }
  },
  // Function fetching the data through requests to the API via other functions, depending on the projects requested by the user
  async fetch() {
    this.$emit('spinner');
    this.loaded = false;
    this.projects = [];
    this.projects_participated = [];
    this.projects_liked = [];
    this.projects_commented = [];
    this.project_type_id = await this.getProjectType();
    let data = { name: 'Pétition' };
    let response = await this.$axios.get('project_type', { params: data });
    this.petition_type_id = response.data['id_project_type'];
    data = { name: 'Consultation' };
    response = await this.$axios.get('project_type', { params: data });
    this.consultation_type_id = response.data['id_project_type'];
    data = { name: 'Conseil de quartier' };
    response = await this.$axios.get('project_type', { params: data });
    this.conseil_type_id = response.data['id_project_type'];
    await this.setImage();
    if (this.my_projects === 'true') {
      if (this.published === 'true') {
        this.projects = await this.getMyPublishedProjects();
      } else {
        this.projects = await this.getMyNOTPublishedProjects();
      }
    } else if (this.participated === 'false') {
      this.projects = await this.getProjects();
      console.log('PROJECTS ', this.projects);
    } else {
      if (this.project_type_id === this.petition_type_id) {
        this.projects_liked = await this.getProjectsLiked();
        const comments = await this.getProjectsCommented();
        await this.sortComments(comments);
      } else {
        const response = await this.getUserAnswers();
        await this.sortUserAnswers(response);
      }
    }
    // console.log('PROJECTS  ', this.projects);
    const delay = ms => new Promise(res => setTimeout(res, ms));
    this.$emit('loaded');
    await delay(2000);
    this.loaded = true;
    this.$nuxt.refresh;
  }
};
</script>

<style scoped>
.project {
  padding-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  max-width: 100%;
  justify-content: center;
  align-content: space-between;
  margin: auto;
}
.group {
  padding: 1rem 1rem;
}
.card {
  max-width: 30rem;
  border: 0.15rem solid rgb(0, 14, 116);
  box-shadow: 6px -2px rgb(0, 14, 116);
}
#description {
  text-align: justify;
  height: 7rem;
  overflow: hidden;
  mask-image: linear-gradient(to bottom, black 20%, transparent 100%);
  white-space: pre-wrap;
}
.noresult {
  text-align: center;
  margin-top: 5rem;
}
.button {
  color: rgb(247, 247, 247);
  background-color: rgb(0, 14, 116);
}
.button:hover {
  color: rgb(0, 14, 116);
  background-color: rgb(247, 247, 247);
}
.pre-formatted {
  white-space: pre;
}
@media (max-width: 1200px) {
  .project {
    padding-top: 0rem;
    max-width: 90%;
  }
  .group {
    padding: 0.5rem;
  }
}
</style>
