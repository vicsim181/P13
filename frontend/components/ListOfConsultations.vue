<template>
  <div>
    <button @click="$fetch">Rafraîchir</button>
    <div v-if="projects">
      <div
        class="column h-100 w-auto project"
        v-for="project in projects"
        :key="project.id_project"
      >
        <nuxt-link :to="`projet/${project.id_project}`">
          {{ project.name }}
        </nuxt-link>
        <p>{{ project.place }}</p>
        <p>{{ project.description }}</p>
      </div>
    </div>
    <div v-else>
      <div class="row h-100 w-auto justify-content-center text-center">
        <h3>Pas de consultation disponible pour le moment</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      projects: null,
      consultation_type: null
    };
  },
  methods: {
    async getConsultationType() {
      const data = { name: 'Consultation' };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    }
  },
  async fetch() {
    this.consultation_type = await this.getConsultationType();
    this.projects = await fetch(
      `http://127.0.0.1:8000/project/?project_type=${this.consultation_type}&ready_for_publication=true`
    ).then(res => res.json());
  }
};
</script>

<style>
.project {
  background-color: aqua;
}
</style>
