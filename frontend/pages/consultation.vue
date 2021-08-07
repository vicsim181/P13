<template>
  <div v-if="this.project" v-bind="this.project">
    <p>{{ this.project.name }}</p>
    <p>{{ this.project.place }}</p>
    <p>{{ this.project.question }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id_project: this.$route.params['id_project'],
      project: null,
      questions: []
    };
  },
  async fetch() {
    this.project = await fetch(
      `http://127.0.0.1:8000/project/${this.id_project}`
    ).then(res => res.json());
  }
};
</script>

<style></style>
