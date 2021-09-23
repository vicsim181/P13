<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      {{ button_label }}
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de pétition"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          label="Nom de la pétition"
          label-for="name-input"
          invalid-feedback="Vous devez donner un nom à la pétition"
          :state="nameState"
        >
          <b-form-input
            id="name-input"
            v-model="petition.name"
            :state="nameState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Lieu concerné"
          label-for="place-input"
          invalid-feedback="Entrez un lieu concerné par la pétition"
          :state="placeState"
        >
          <b-form-input
            id="place-input"
            v-model="petition.place"
            :state="placeState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="Description de la pétition"
          label-for="description-input"
          invalid-feedback="Décrivez la pétition"
          :state="descriptionState"
        >
          <b-form-textarea
            id="description-input"
            v-model="petition.description"
            :state="descriptionState"
            required
          ></b-form-textarea>
        </b-form-group>
      </form>
      <template #modal-footer="{cancel}">
        <b-button size="lg" variant="primary" @click="handleQuitPetition()">
          Sauvegarder et quitter
        </b-button>
        <b-button size="lg" variant="danger" @click="cancel()">
          Annuler
        </b-button>
      </template>
    </b-modal>

    <!-- SECOND MODAL FOR CONFIRMATION -->
    <b-modal id="modal-validation" title="Pétition sauvegardée" hide-footer>
      <div class="d-block text-center">
        <h3>
          Votre projet de pétition est sauvegardé et accessible depuis votre
          profil, mes pétitions, non publiées.
        </h3>
      </div>
      <b-button
        class="mt-3 button"
        block
        @click="$bvModal.hide('modal-validation')"
        >Ok</b-button
      >
    </b-modal>
  </div>
</template>

<script>
export default {
  props: ['button'],
  computed: {
    nameState() {
      return this.petition.name.length > 0 ? true : false;
    },
    placeState() {
      return this.petition.place.length > 0 ? true : false;
    },
    descriptionState() {
      return this.petition.description.length > 0 ? true : false;
    }
  },
  data() {
    return {
      button_label: this.button,
      petition: {
        name: '',
        place: '',
        description: '',
        project_type: ''
      },
      id_project: '',
      id_owner: ''
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
      this.petition.name = '';
      this.petition.place = '';
      this.petition.description = '';
    },

    // We send a POST request to the API with the data about the Petition
    async getPetitionType() {
      const data = { name: 'Pétition' };
      const response = await this.$axios.get('project_type', { params: data });
      const type_id = response.data['id_project_type'];
      return type_id;
    },

    // We send a POST request to the API with the data about the Conseil
    async postPetitionData() {
      const data = {
        name: this.petition.name,
        place: this.petition.place,
        description: this.petition.description,
        project_type: this.projectType
      };
      try {
        const response = await this.$axios.post('project/', data);
        console.log(response.data);
        this.id_project = response.data['id_project'];
        this.id_owner = response.data['owner'];
      } catch (error) {
        console.log(error.response);
        const keys = Object.keys(error.response.data);
        const errorMessage = error.response.data[keys[0]];
        window.alert(errorMessage);
      }
    },

    // FUNCTIONS CALLED BY THE BUTTONS

    // Alternative to handleOkPetition() in the case we want to quit (only saving) instead of publishing
    handleQuitPetition() {
      this.handleSubmit();
    },
    // Function called by the previous ones, taking care of the different steps
    async handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getPetitionType();
      await this.postPetitionData();
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
        this.$bvModal.show('modal-validation');
      });
    }
  }
};
</script>
