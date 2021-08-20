<template>
  <div v-if="loaded">
    <div v-if="projects.length > 0" class="project">
      <b-card-group
        v-for="project in projects"
        :key="project.id_project"
        class="group"
      >
        <b-card
          img-src="https://picsum.photos/600/300/?image=25"
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
                <b-card-text id="description">{{
                  project.description
                }}</b-card-text>
              </li>
              <br />
              <li>
                <b-card-text>
                  Publié le : {{ project.publication }}
                </b-card-text>
              </li>
              <div v-if="project.is_over">
                <li>
                  <b-card-text> Terminé </b-card-text>
                </li>
              </div>
              <div v-else>
                <li>
                  <b-card-text> En cours </b-card-text>
                  <b-card-text> Fin le {{ project.end_date }} </b-card-text>
                </li>
              </div>
              <div v-if="project_type === 'Pétition'">
                <li>
                  Pétition soutenue par:
                  {{ project.liked_by.length }} personne(s).
                </li>
              </div>
            </ul>
            <b-button
              squared
              class="align-self-end btn btn-lg btn-block btn-outline-primary"
              style="margin-top: auto;"
              :to="`/projet/${project.id_project}`"
              variant="outline"
              >Consulter</b-button
            >
          </div>
        </b-card>
      </b-card-group>
    </div>
    <div v-else id="noresult">
      <p>Aucun projet trouvé</p>
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
      loaded: false,
      project_type_id: null,
      projects: [],
      projects_participated: []
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
    }
  },
  async fetch() {
    console.log('START FETCHING');
    this.$emit('spinner');
    this.loaded = false;
    this.projects = [];
    this.projects_participated = [];
    this.project_type_id = await this.getProjectType();
    if (this.my_projects === 'true') {
      this.projects = await fetch(
        `http://127.0.0.1:8000/project/?project_type=${this.project_type_id}&ready_for_publication=${this.published}&owner_id=${this.loggedInUser.id}`
      ).then(res => res.json());
    } else if (this.participated === 'false') {
      this.projects = await fetch(
        `http://127.0.0.1:8000/project/?project_type=${this.project_type_id}&ready_for_publication=${this.published}`
      ).then(res => res.json());
    } else {
      const response = await fetch(
        `http://127.0.0.1:8000/user_answer/?user=${this.loggedInUser.id}`
      ).then(res => res.json());
      if (response.length !== 0) {
        for (const element in response) {
          const question = await this.$axios.get(
            `question/${response[element].question}`
          );
          const project = await this.$axios.get(
            `project/${question.data.project}`
          );
          if (
            project.data.project_type === this.project_type_id &&
            !this.projects.some(
              element => element.id_project == project.data.id_project
            )
          ) {
            this.projects.push(project.data);
          }
        }
      }
    }
    const delay = ms => new Promise(res => setTimeout(res, ms));
    this.$emit('loaded');
    await delay(2000);
    this.loaded = true;
    console.log('LOADED');
    console.log('PROJECTS ', this.projects);
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
}
#noresult {
  text-align: center;
  margin-top: 5rem;
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
