<template>
  <body>
    <div class="container">
      <div class="title">
        <h1>Inscription</h1>
      </div>
      <div class="row h-100 w-auto justify-content-center text-center">
        <b-form
          @submit="onSubmit"
          @reset="onReset"
          v-show="show"
          validated
          novalidate
        >
          <b-form-group id="input-group-3" label="Prénom:" label-for="input-3">
            <b-form-input
              id="input-3"
              type="text"
              v-model="form.first_name"
              placeholder="Entrez votre prénom"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-4"
            label="Nom de famille:"
            label-for="input-4"
          >
            <b-form-input
              id="input-4"
              type="text"
              v-model="form.last_name"
              placeholder="Entrez votre nom de famille"
              required
            ></b-form-input>
          </b-form-group>

          <b-form-group
            id="input-group-1"
            label="Adresse Email:"
            label-for="input-1"
          >
            <b-form-input
              id="input-1"
              v-model="form.email"
              type="email"
              placeholder="Entrez votre adresse email"
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
              placeholder="Entrez un mot de passe"
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
  name: 'Signup',
  data() {
    return {
      form: {
        email: '',
        password: '',
        first_name: '',
        last_name: ''
      },
      show: true
    };
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault();
      const data = this.form;
      console.log('THIS FORM  :', data);
      try {
        const response = await $axios.$post('users/', data);
        console.log(response);
        this.$router.push('/');
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
      this.form.first_name = '';
      this.form.last_name = '';
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
