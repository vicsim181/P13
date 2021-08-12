<template>
  <div>
    <b-button v-b-modal.modal-prevent-closing-1 variant="dark">
      Créer une pétition
    </b-button>

    <b-modal
      id="modal-prevent-closing-1"
      size="lg"
      ref="modal"
      title="Création de pétition"
      ok-title="Valider et publier la pétition"
      ok-variant="primary"
      cancel-title="Annuler"
      cancel-variant="danger"
      no-close-on-backdrop
      header-bg-variant="dark"
      header-text-variant="light"
      button-size="lg"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOkPetition"
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
        <b-form-group
          label="Une pétition a une durée de vie de 90 jours à partir de sa publication"
        >
        </b-form-group>
        <b-form-group label="Enregistrer la pétition et quitter">
          <div modal-footer="Valider la pétition">
            <b-button
              id="save_quit"
              size="lg"
              variant="primary"
              @click="handleQuitPetition()"
            >
              Publier plus tard
            </b-button>
          </div>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
export default {
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
      publish: false,
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
      this.publish = false;
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

    // We send a PUT request to the API with the id of the Conseil project to publish it
    publishPetition() {
      this.$axios.put('publication', { project_id: this.id_project });
    },

    // FUNCTIONS CALLED BY THE BUTTONS

    // We call this function when clicking on one of the 3 buttons (Save and quit, Publish and quit, add a question)
    handleOkPetition(bvModalEvt) {
      bvModalEvt.preventDefault();
      if (!this.checkFormValidity()) {
        console.log('HANDLE QUIT CHECK FORM INVALID');
        return;
      } else {
        console.log('HANDLE QUIT CHECK FORM VALID');
        this.publish = true;
        this.handleSubmit();
      }
    },
    // Alternative to handleOkPetition() in the case we want to quit (only saving) instead of publishing
    handleQuitPetition() {
      if (!this.checkFormValidity()) {
        console.log('HANDLE QUIT CHECK FORM INVALID');
        return;
      } else {
        console.log('HANDLE QUIT CHECK FORM VALID');
        this.handleSubmit();
      }
    },
    // Function called by the previous ones, taking care of the different steps
    async handleSubmit() {
      if (!this.checkFormValidity()) {
        return;
      }
      this.projectType = await this.getPetitionType();
      await this.postPetitionData();
      if (this.publish == true) {
        this.publishPetition();
      }
      this.$nextTick(() => {
        this.$bvModal.hide('modal-prevent-closing-1');
      });
    }
  }
};
</script>
