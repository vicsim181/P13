<template>
  <div>
    <button @click="$fetch">Rafraîchir</button>
    <div v-if="projects">
      <div
        class="column h-100 w-auto project"
        v-for="project in projects"
        :key="project.id_project"
      >
        <router-link
          :to="{
            name: 'project',
            params: { id_project: project.id_project }
          }"
        >
          <p>{{ project.name }}</p>
        </router-link>
        <p>{{ project.place }}</p>
        <p>{{ project.description }}</p>
      </div>
    </div>
    <div v-else>
      <div class="row h-100 w-auto justify-content-center text-center">
        <h3>Pas de conseil disponible pour le moment</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      projects: null,
      conseil_type: null
    };
  },
  methods: {
    async getConseilType() {
      const data = { name: 'Conseil de quartier' };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    }
  },
  async fetch() {
    this.conseil_type = await this.getConseilType();
    this.projects = await fetch(
      `http://127.0.0.1:8000/project/?project_type=${this.conseil_type}&ready_for_publication=true`
    ).then(res => res.json());
  }
};
</script>

<style>
.project {
  background-color: aqua;
}
</style>
