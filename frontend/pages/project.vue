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
      <div class="row" v-if="project.question.length != 0">
        <p>Questions:</p>
        <p>{{ this.project.question }}</p>
      </div>
    </div>
    <CustomFooter />
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
