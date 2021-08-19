<template>
  <div>
    <CustomNavbar />
    <div class="container">
      <div class="h-100 justify-content-center text-center">
        <h1>Mes pétitions</h1>
      </div>
      <br />
      <b-button @click="participated()"
        >Les pétitions auxquelles j'ai participé</b-button
      >
      <b-button @click="published()">Mes pétitions publiées</b-button>
      <b-button @click="not_published()">Mes pétitions non publiées</b-button>
      <br />
      <div v-if="petitions_participated">
        <ListOfProjects
          project_type="Pétition"
          my_projects="false"
          published="true"
          participated="true"
        />
      </div>
      <div v-if="petitions_published">
        <ListOfProjects
          project_type="Pétition"
          my_projects="true"
          published="true"
          participated="false"
        />
      </div>
      <div v-if="petitions_not_published">
        <ListOfProjects
          project_type="Pétition"
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
      petitions_participated: true,
      petitions_published: false,
      petitions_not_published: false
    };
  },
  methods: {
    participated() {
      this.petitions_participated = true;
      this.petitions_published = false;
      this.petitions_not_published = false;
      console.log('participated ', this.petitions_participated);
      console.log('published ', this.petitions_published);
      console.log('not published ', this.petitions_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    },
    published() {
      this.petitions_participated = false;
      this.petitions_published = true;
      this.petitions_not_published = false;
      console.log('participated ', this.petitions_participated);
      console.log('published ', this.petitions_published);
      console.log('not published ', this.petitions_not_published);
      console.log('REFRESH');
      this.$nuxt.refresh();
    },
    not_published() {
      this.petitions_participated = false;
      this.petitions_published = false;
      this.petitions_not_published = true;
      console.log('participated ', this.petitions_participated);
      console.log('published ', this.petitions_published);
      console.log('not published ', this.petitions_not_published);
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
