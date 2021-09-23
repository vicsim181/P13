<template>
  <ListOfProjects
    :project_type="project_type_name"
    my_projects="false"
    published="true"
    participated="true"
    v-on:spinner="spinner()"
    v-on:loaded="loaded()"
  ></ListOfProjects>
</template>

<script>
export default {
  props: ['project_type'],
  data() {
    return { project_type_name: this.project_type };
  },
  methods: {
    loaded() {
      this.$emit('loaded');
    },
    spinner() {
      this.$emit('spinner');
    }
  }
};
</script>

<style></style>
