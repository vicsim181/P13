<template>
  <div>
    <b-button v-b-modal.modal-address class="button">
      Enregistrer votre addresse
    </b-button>

    <b-modal
      id="modal-address"
      size="lg"
      ref="modal"
      title="Enregistrer votre adresse"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Numéro"
          label-for="num-input"
          invalid-feedback="Vous devez renseignez un numéro compris entre 1 et 10 000 inclus"
          :state="numState"
        >
          <b-form-input
            id="num-input"
            v-model="address.num"
            :state="numState"
            :number="true"
            type="number"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Nom de rue"
          label-for="street-input"
          invalid-feedback="Entrez un nom de rue"
          :state="streetState"
        >
          <b-form-input
            id="street-input"
            v-model="address.street"
            :state="streetState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Commune"
          label-for="city-input"
          invalid-feedback="Entrez un nom de commune"
          :state="cityState"
        >
          <b-form-input
            id="city-input"
            v-model="address.city"
            :state="cityState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Code postal"
          label-for="postal-input"
          invalid-feedback="Entrez le code postal"
          :state="postalState"
        >
          <b-form-input
            id="postal-input"
            v-model="address.postal_code"
            :state="postalState"
            :number="true"
            type="number"
            required
          ></b-form-input>
        </b-form-group>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="success" @click="handleOkAddress()">
          Sauvegarder mon adresse
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  computed: {
    numState() {
      return (
        typeof this.address.num === 'number' &&
        this.address.num.toString().length < 6 &&
        this.address.num > 0 &&
        this.address.num < 10001
      );
    },
    streetState() {
      return this.address.street.length > 0;
    },
    cityState() {
      return this.address.city.length > 0;
    },
    postalState() {
      return (
        typeof this.address.postal_code === 'number' &&
        this.address.postal_code.toString().length === 5 &&
        this.address.postal_code > 0 &&
        this.address.postal_code < 100000
      );
    }
  },
  data() {
    return {
      publish: false,
      address: {
        num: null,
        complement: '',
        street: '',
        city: '',
        postal_code: null
      }
    };
  },
  methods: {
    // We check the form with the infos of the Petition is valid
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      return valid;
    },

    // We reset the data of the first form, the Petition basic infos
    resetModal() {
      this.address.num = null;
      this.address.complement = '';
      this.address.street = '';
      this.address.city = '';
      this.address.postal_code = null;
    },

    // FUNCTIONS CALLED BY THE BUTTONS

    // Function called when save button pressed, taking care of the different steps
    async handleOkAddress() {
      if (!this.checkFormValidity()) {
        return;
      }
      const data = {
        num: this.address.num,
        street: this.address.street,
        city: this.address.city,
        postal_code: this.address.postal_code
      };
      try {
        const response = await this.$axios.post('address/', data);
        console.log(response.data);
      } catch (error) {
        console.log(error.response.data);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
      this.$nextTick(() => {
        this.$bvModal.hide('modal-address');
      });
    }
  }
};
</script>
<style>
.button {
  color: rgb(247, 247, 247);
  background-color: rgb(0, 14, 116);
}
.button:hover {
  color: rgb(0, 14, 116);
  background-color: rgb(247, 247, 247);
}
</style>
