<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="h-100 justify-content-center text-center">
        <h1>Mes conseils de quartier</h1>
      </div>
      <br />
      <b-button @click="participated()"
        >Les conseils de quartier auxquelles j'ai participé</b-button
      >
      <b-button @click="published()" v-if="loggedInUser.is_staff"
        >Mes conseils de quartier publiées</b-button
      >
      <b-button @click="not_published()" v-if="loggedInUser.is_staff"
        >Mes conseils de quartier non publiées</b-button
      >
      <br />
      <div v-if="conseil_participated">
        <ListOfProjects
          project_type="Conseil de quartier"
          my_projects="false"
          published="true"
          participated="true"
        />
      </div>
      <div v-if="conseil_published">
        <ListOfProjects
          project_type="Conseil de quartier"
          my_projects="true"
          published="true"
          participated="false"
        />
      </div>
      <div v-if="conseil_not_published">
        <ListOfProjects
          project_type="Conseil de quartier"
          my_projects="true"
          published="false"
          participated="false"
        />
      </div>
    </div>
    <CustomFooter />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  auth: false,
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  },
  data() {
    return {
      conseil_participated: false,
      conseil_published: false,
      conseil_not_published: false
    };
  },
  methods: {
    participated() {
      this.conseil_participated = true;
      this.conseil_published = false;
      this.conseil_not_published = false;
      console.log('participated ', this.conseil_participated);
      console.log('published ', this.conseil_published);
      console.log('not published ', this.conseil_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    },
    published() {
      this.conseil_participated = false;
      this.conseil_published = true;
      this.conseil_not_published = false;
      console.log('participated ', this.conseil_participated);
      console.log('published ', this.conseil_published);
      console.log('not published ', this.conseil_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    },
    not_published() {
      this.conseil_participated = false;
      this.conseil_published = false;
      this.conseil_not_published = true;
      console.log('participated ', this.conseil_participated);
      console.log('published ', this.conseil_published);
      console.log('not published ', this.conseil_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    }
    // refresh() {
    //   console.log('participated ', this.consultations_participated);
    //   console.log('published ', this.consultations_published);
    //   console.log('not published ', this.consultations_not_published);
    //   console.log('REFRESH');
    //   this.$nuxt.refresh();
    // }
  },
  middleware: 'auth'
};
</script>

<style>
.container {
  min-width: 100%;
  padding-top: 15rem;
  padding-bottom: 10rem;
  color: rgb(0, 14, 116);
}
</style>
