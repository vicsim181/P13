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
    const data = { owner_id: this.user_id };
    const response = await this.$axios.get('http://127.0.0.1:8000/project', {
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
