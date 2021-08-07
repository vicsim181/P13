<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="row h-100 w-auto justify-content-center">
        {{ user_id }}
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
    const data = { ready_for_publication: 'false' };
    const response = await this.$axios.get('project', { params: data });
    console.log(response);
  }
};
</script>

<style>
.container {
  padding-top: 15rem;
}
</style>
