<template>
  <div class="container">
      <div class="row" v-for="project in projects">
          <p>Rien</p>
      </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      projects: []
    };
  },
  created() {
    // fetch the data when the view is created and the data is
    // already being observed
    this.getProjectsList();
  },
  watch: {
    // call again the method if the route changes
    $route: "getProjectsList"
  },
  methods: {
    async getProjectsList() {
      const response = await this.$axios.get("project");
      console.log("PROJECTS LIST:    ", response);
    }
  }
};
</script>

<style></style>
