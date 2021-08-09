<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="row h-100 w-auto justify-content-center">
        {{ projects }}
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
export default {
  data() {
    return { user_id: this.$route.params['owner_id'], projects: [] };
  },
  async fetch() {
    const response_1 = await this.$axios.get('project_type', {
      params: { name: 'Consultation' }
    });
    const consultation_type = response_1.data['id_project_type'];
    console.log(consultation_type);
    const data = { owner_id: this.user_id, project_type: consultation_type };
    const response = await this.$axios.get('project', {
      params: data
    });
    this.projects = response.data;
    console.log(this.projects);
  }
};
</script>

<style>
.container {
  padding-top: 15rem;
}
</style>
