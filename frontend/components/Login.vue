<template>
  <body>
    <div class="container">
      <div class="title">
        <h1>Connexion</h1>
      </div>
      <div class="row h-100 w-auto justify-content-center text-center">
        <b-form
          @submit="onSubmit"
          @reset="onReset"
          v-if="show"
          validated
          novalidate
        >
          <b-form-group
            id="input-group-1"
            label="Adresse Email:"
            label-for="input-1"
          >
            <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              placeholder="Adresse email"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-2"
            label="Mot de passe:"
            label-for="input-2"
          >
            <b-form-input
              id="input-2"
              type="password"
              v-model="form.password"
              placeholder="Mot de passe"
              required
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Valider</b-button>
          <b-button type="reset" variant="danger">Effacer</b-button>
        </b-form>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      show: true
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const data = this.form;
      console.log(data);
      try {
        const response = await this.$axios.post('login/', data);
        console.log(response);
      } catch (error) {
        console.log(error.response.data);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.email = '';
      this.form.password = '';
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  }
};
</script>

<style>
body {
  min-width: 100%;
  padding-top: 6rem;
  padding-bottom: 7rem;
  color: rgb(0, 14, 116);
}
.title {
  text-align: center;
}
</style>
