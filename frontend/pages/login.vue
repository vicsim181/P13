<template>
  <div class="main">
    <!-- <form class="">
      <div id="input-group-1" role="group" class="form-group">
        <label id="input-group-1__BV_label_" for="input-1" class="d-block"
          >Email address:</label
        >
        <div>
          <input
            id="input-1"
            type="email"
            placeholder="Enter email"
            required="required"
            aria-required="true"
            class="form-control"
            aria-describedby="input-group-1__BV_description_"
          />
        </div>
      </div>
      <div id="input-group-2" role="group" class="form-group">
        <label id="input-group-2__BV_label_" for="input-2" class="d-block"
          >Your Password:</label
        >
        <div>
          <input
            id="input-2"
            type="password"
            placeholder="Enter password"
            required="required"
            aria-required="true"
            class="form-control"
          />
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
      <button type="reset" class="btn btn-danger">Reset</button>
    </form> -->
    <b-form
      @submit="onSubmit"
      @reset="onReset"
      v-if="show"
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
        label="Addresse Email:"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Entrez votre addresse email"
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
      <b-form-group
        id="input-group-5"
        label="Confirmation du mot de passe:"
        label-for="input-5"
      >
        <b-form-input
          id="input-5"
          type="password"
          v-model="form.password"
          placeholder="Confirmez votre mot de passe"
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Valider</b-button>
      <b-button type="reset" variant="danger">Effacer</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        email: '',
        password: ''
      },
      show: true
    };
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      // alert(JSON.stringify(this.form));
      console.log(JSON.stringify(this.form));
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
.main {
  padding-top: 5rem;
  max-width: 90%;
  padding-left: 2rem;
}
</style>
