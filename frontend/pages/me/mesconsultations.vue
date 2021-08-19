<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="h-100 justify-content-center text-center">
        <h1>Mes consultations</h1>
      </div>
      <br />
      <b-button @click="participated()"
        >Les consultations auxquelles j'ai participé</b-button
      >
      <b-button @click="published()" v-if="loggedInUser.is_staff"
        >Mes consultations publiées</b-button
      >
      <b-button @click="not_published()" v-if="loggedInUser.is_staff"
        >Mes consultations non publiées</b-button
      >
      <br />
      <div v-if="consultations_participated">
        <ListOfProjects
          project_type="Consultation"
          my_projects="false"
          published="true"
          participated="true"
        />
      </div>
      <div v-if="consultations_published">
        <ListOfProjects
          project_type="Consultation"
          my_projects="true"
          published="true"
          participated="false"
        />
      </div>
      <div v-if="consultations_not_published">
        <ListOfProjects
          project_type="Consultation"
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
      consultations_participated: true,
      consultations_published: false,
      consultations_not_published: false
    };
  },
  methods: {
    participated() {
      this.consultations_participated = true;
      this.consultations_published = false;
      this.consultations_not_published = false;
      console.log('participated ', this.consultations_participated);
      console.log('published ', this.consultations_published);
      console.log('not published ', this.consultations_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    },
    published() {
      this.consultations_participated = false;
      this.consultations_published = true;
      this.consultations_not_published = false;
      console.log('participated ', this.consultations_participated);
      console.log('published ', this.consultations_published);
      console.log('not published ', this.consultations_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    },
    not_published() {
      this.consultations_participated = false;
      this.consultations_published = false;
      this.consultations_not_published = true;
      console.log('participated ', this.consultations_participated);
      console.log('published ', this.consultations_published);
      console.log('not published ', this.consultations_not_published);
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
